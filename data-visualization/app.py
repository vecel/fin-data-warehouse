import os
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = os.getenv("API_URL", "http://data-serving:8000")

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

instruments_df = fetch_available_instruments()

if instruments_df.empty:
    st.info("No records loaded. Please verify that data ingestion pipeline has successfully processed source files.")
else:
    st.sidebar.header("Configuration Panel")
    instruments_df['display_label'] = instruments_df['instrument_code'] + " - " + instruments_df['instrument_short_name']
    
    selected_label = st.sidebar.selectbox("Choose Financial Asset:", instruments_df['display_label'].tolist())
    
    chosen_record = instruments_df[instruments_df['display_label'] == selected_label].iloc[0]
    ticker_code = chosen_record['instrument_code']

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric(label="Selected Symbol", value=ticker_code)
    with kpi_col2:
        st.metric(label="Market Exchange", value=chosen_record['instrument_market_name'])
    with kpi_col3:
        st.metric(label="Price Level Category", value=chosen_record['instrument_price_category'])
    with kpi_col4:
        st.metric(label="Yearly Performance Shift", value=chosen_record['yearly_price_change_category'])

    st.markdown("### Interactive Analytical Views")
    tab_market, tab_sentiment, tab_profile = st.tabs(["📈 Market Candlestick Trends", "📰 News Feed & Sentiment Analysis", "💼 Corporate Profile"])

    with tab_market:
        st.subheader("Historical Stock Price Actions")
        quotes_df = fetch_historical_quotes(ticker_code)
        
        if quotes_df.empty:
            st.warning(f"No pricing factual data registered inside the warehouse for symbol {ticker_code}")
        else:
            candlestick_fig = go.Figure(data=[go.Candlestick(
                x=quotes_df['quote_date'],
                open=quotes_df['open_price'],
                high=quotes_df['high_price'],
                low=quotes_df['low_price'],
                close=quotes_df['close_price'],
                name=ticker_code
            )])
            candlestick_fig.update_layout(
                template="plotly_dark",
                xaxis_rangeslider_visible=True,
                margin=dict(l=20, r=20, t=20, b=20),
                height=500
            )
            st.plotly_chart(candlestick_fig, use_container_width=True)
            
            with st.expander("View Raw Warehouse Facts Table (dwh.quote_fact)"):
                st.dataframe(quotes_df.sort_values('quote_date', ascending=False), use_container_width=True)

    with tab_sentiment:
        st.subheader("Market Sentiment Tracker")
        news_df = fetch_correlated_news(ticker_code)
        
        if news_df.empty:
            st.info(f"No indexed news headlines found in the database for asset {ticker_code}")
        else:
            for _, article in news_df.iterrows():
                score = article['instrument_sentiment_value']
                badge_color = "green" if score > 0.15 else "red" if score < -0.15 else "orange"
                
                st.markdown(f"#### 🔗 [{article['news_title_name']}]({article['source_link']})")
                st.markdown(f"**Publisher:** {article['source_name']} | **Date Tracked:** {article['published_date']}")
                st.markdown(
                    f"Asset Sentiment Index: :{badge_color}[{article['instrument_sentiment_name']} ({score})] | "
                    f"Global Macro Score: {article['aggregated_news_sentiment_name']} ({article['aggregated_news_sentiment_value']})"
                )
                st.divider()

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