import os
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = os.getenv("API_URL", "http://data-serving:8040")

st.set_page_config(
    page_title="Financial Data Warehouse Portal",
    page_icon="📉",
    layout="wide"
)

st.title("📊 Financial Data Warehouse Portal")
st.markdown("Automated end-to-end analytical data-pipeline visualization engine.")
st.divider()

@st.cache_data(ttl=30)
def fetch_available_instruments():
    """Fetch list of companies tracked inside the system."""
    try:
        response = requests.get(f"{API_URL}/api/instruments", timeout=5)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Connection Alert: Unable to reach REST API server at {API_URL}. Details: {e}")
    return pd.DataFrame()

def fetch_historical_quotes(ticker):
    """Retrieve financial history metrics for the chosen asset."""
    try:
        response = requests.get(f"{API_URL}/api/quotes?ticker={ticker}&limit=300", timeout=5)
        if response.status_code == 200:
            res_data = response.json()
            if res_data:
                df = pd.DataFrame(res_data)
                df['quote_date'] = pd.to_datetime(df['quote_date'])
                return df.sort_values('quote_date')
    except Exception as e:
        st.error(f"API Error: Failed to download historical metrics for {ticker}: {e}")
    return pd.DataFrame()

def fetch_correlated_news(ticker):
    """Retrieve indexed articles and parsed AI sentiments."""
    try:
        response = requests.get(f"{API_URL}/api/news?ticker={ticker}&limit=25", timeout=5)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"API Error: Failed to download news logs for {ticker}: {e}")
    return pd.DataFrame()

def fetch_macro_data(country_code):
    """Retrieve raw macroeconomic indicators processed from FRED datasets."""
    try:
        response = requests.get(f"{API_URL}/api/macro?country_code={country_code}&limit=1000", timeout=5)
        if response.status_code == 200:
            res_data = response.json()
            if res_data:
                df = pd.DataFrame(res_data)
                df['declaration_date'] = pd.to_datetime(df['declaration_date'])
                return df.sort_values('declaration_date')
    except Exception as e:
        st.error(f"API Error: Failed to download macro metrics for {country_code}: {e}")
    return pd.DataFrame()

instruments_df = fetch_available_instruments()

if instruments_df.empty:
    st.info("No records loaded. Please verify that data ingestion pipeline has successfully processed source files.")
else:
    st.sidebar.header("Configuration Panel")
    instruments_df['display_label'] = instruments_df['instrument_code'] + " - " + instruments_df['instrument_short_name']
    
    selected_label = st.sidebar.selectbox("Choose Financial Asset:", instruments_df['display_label'].tolist())
    
    chosen_record = instruments_df[instruments_df['display_label'] == selected_label].iloc[0]
    ticker_code = chosen_record['instrument_code']

    is_poland = ticker_code.endswith(".WA")
    currency_code = "PLN" if is_poland else "USD"

    kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(4)
    with kpi_col2:
        st.metric(label="Market Exchange", value=chosen_record['instrument_market_name'])
    with kpi_col3:
        st.metric(label="Price Level Category", value=chosen_record['instrument_price_category'])
    with kpi_col4:
        st.metric(label="Yearly Performance Shift", value=chosen_record['yearly_price_change_category'])
    with kpi_col5:
        st.metric(label="Currency", value=currency_code)

    st.markdown("### Interactive Analytical Views")
    tab_market, tab_macro, tab_profile = st.tabs(["📈 Market Candlestick Trends", "🌍 Country Macroeconomic Indicators", "🏢 Corporate Profile"])

    with tab_market:
        st.subheader("Historical Stock Price Actions")
        quotes_df = fetch_historical_quotes(ticker_code)
        
        if quotes_df.empty:
            st.warning(f"No pricing factual data registered inside the warehouse for symbol {ticker_code}")
        else:
            price_fig = go.Figure()
            
            price_fig.add_trace(go.Scatter(
                x=quotes_df['quote_date'],
                y=quotes_df['open_price'],
                mode='lines+markers',
                name='Opening price',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=6)
            ))
            
            price_fig.add_trace(go.Scatter(
                x=quotes_df['quote_date'],
                y=quotes_df['close_price'],
                mode='lines+markers',
                name='Closing price',
                line=dict(color='#ff7f0e', width=2),
                marker=dict(size=6)
            ))
            
            price_fig.update_layout(
                template="plotly_dark",
                xaxis_title="Date",
                yaxis_title="Stock price",
                margin=dict(l=20, r=20, t=20, b=20),
                height=500,
                hovermode="x unified"
            )
            
            st.plotly_chart(price_fig, use_container_width=True)
            
            with st.expander("View Raw Warehouse Facts Table (dwh.quote_fact)"):
                st.dataframe(quotes_df.sort_values('quote_date', ascending=False), use_container_width=True)
    
    with tab_macro:
        st.subheader("Macroeconomic Trends Context")
        
        country_iso = "PL" if ticker_code.endswith(".WA") else "US"
        
        macro_df = fetch_macro_data(country_iso)
        
        if macro_df.empty:
            st.info(f"No macroeconomic trends synchronized inside the warehouse for country context: {country_iso}")
        else:
            available_indicators = macro_df['indicator_name'].unique().tolist()
            selected_indicator = st.selectbox("Choose Macro Indicator to Plot:", available_indicators)
            
            filtered_macro = macro_df[macro_df['indicator_name'] == selected_indicator]
            
            macro_fig = go.Figure()
            macro_fig.add_trace(go.Scatter(
                x=filtered_macro['declaration_date'],
                y=filtered_macro['indicator_value'],
                mode='lines+markers',
                name=selected_indicator,
                line=dict(color='#00CC96', width=2)
            ))
            macro_fig.update_layout(
                template="plotly_dark",
                xaxis_title="Timeline",
                yaxis_title="Value Index",
                margin=dict(l=20, r=20, t=20, b=20),
                height=450
            )
            st.plotly_chart(macro_fig, use_container_width=True)

    with tab_profile:
        st.subheader("Dimension Attributes Summary")
        profile_matrix = {
            "Dimension Field": ["Surrogate ID Key", "Registered Long Corporate Name", "Economic Sector Group", "Industrial Category", "Pipeline Active Flag"],
            "Warehouse Record Value": [
                chosen_record['instrument_id'],
                chosen_record['instrument_long_name'],
                chosen_record['instrument_sector_name'],
                chosen_record['instrument_industry_name'],
                str(chosen_record['is_active_flag'])
            ]
        }
        st.table(pd.DataFrame(profile_matrix))