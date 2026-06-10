import os
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("financial_dwh_api")

app = FastAPI(
    title="Financial Data Warehouse REST API",
    description="Production API serving enriched stock quotes and FRED macroeconomics data",
    version="1.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL Data Warehouse."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "db"),
            database=os.getenv("POSTGRES_DB", "finance_db"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error(f"Critical: Database connection failed. Details: {e}")
        raise HTTPException(status_code=500, detail="Internal Database connection error")

@app.get("/")
def read_root():
    """Root health-check endpoint."""
    return {
        "status": "healthy",
        "message": "Financial Data Warehouse API operational. Documentation available at /docs"
    }

@app.get("/api/instruments")
def get_instruments():
    """Fetch all financial instruments available inside the warehouse dimension table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT instrument_id, instrument_code, instrument_short_name, instrument_long_name, 
                   instrument_market_name, instrument_sector_name, instrument_industry_name,
                   instrument_price_category, yearly_price_change_category, is_active_flag
            FROM dwh.instrument_dim
            ORDER BY instrument_code;
        """)
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error querying dwh.instrument_dim: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve instruments from warehouse")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/quotes")
def get_quotes(
    ticker: str = Query(None, description="Filter historical stock quotes by asset ticker (e.g., AAPL)"),
    limit: int = Query(100, ge=1, le=1000, description="Limit result dataset row count")
):
    """Fetch historical stock quotes enriched with forward-filled macroeconomic indicators."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT i.instrument_code, d.date::text as quote_date, 
                   q.open_price::numeric as open_price, q.close_price::numeric as close_price, 
                   q.low_price::numeric as low_price, q.high_price::numeric as high_price, 
                   q.volume_number,
                   q.current_gdp, q.current_unemployment, q.current_inflation
            FROM dwh.quote_fact q
            JOIN dwh.instrument_dim i ON q.instrument_id = i.instrument_id
            JOIN dwh.date_dim d ON q.date_id = d.date_id
        """
        params = []
        if ticker:
            query += " WHERE i.instrument_code = %s"
            params.append(ticker.upper())
            
        query += " ORDER BY d.date DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error querying dwh.quote_fact: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stock quotes data")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/macro")
def get_macro_data(
    country_code: str = Query(None, description="Filter macro indicators by country code (e.g., US, PL)"),
    limit: int = Query(200, ge=1, le=2000, description="Limit result dataset row count")
):
    """Fetch raw standalone macroeconomic indicators processed from FRED datasets."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT c.country_code, c.country_name, ind.indicator_code, ind.indicator_name,
                   d.date::text as declaration_date, mf.indicator_value
            FROM dwh.macro_fact mf
            JOIN dwh.country_dim c ON mf.country_id = c.country_id
            JOIN dwh.macro_indicator_dim ind ON mf.indicator_id = ind.indicator_id
            JOIN dwh.date_dim d ON mf.date_id = d.date_id
        """
        params = []
        if country_code:
            query += " WHERE c.country_code = %s"
            params.append(country_code.upper())
            
        query += " ORDER BY d.date DESC, ind.indicator_code LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        return data if data else []
    except Exception as e:
        logger.error(f"Error querying dwh.macro_fact: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve macroeconomic factors")
    finally:
        cursor.close()
        conn.close()