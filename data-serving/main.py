import os
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
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

class InstrumentResponse(BaseModel):
    instrument_id: str = Field(..., description="Klucz surogatowy instrumentu (MD5 Hash)")
    instrument_code: str = Field(..., description="Symbol giełdowy (np. AAPL, PKO.WA)")
    instrument_short_name: str = Field(..., description="Skrócona nazwa spółki")
    instrument_long_name: str = Field(..., description="Pełna nazwa rejestrowa spółki")
    instrument_market_name: str = Field(..., description="Giełda papierów wartościowych")
    instrument_sector_name: str = Field(..., description="Sektor ekonomiczny")
    instrument_industry_name: str = Field(..., description="Branża przemysłowa")
    instrument_price_category: str = Field(..., description="Klasyfikacja poziomu cenowego akcji")
    yearly_price_change_category: str = Field(..., description="Ocena rocznej zmiany rentowności")
    is_active_flag: str = Field(..., description="Flaga aktywności w hurtowni danych (YES/No)")

    class Config:
        json_schema_extra = {
            "example": {
                "instrument_id": "98d73a9860255aedea46f497be336125",
                "instrument_code": "PKO.WA",
                "instrument_short_name": "PKOBP",
                "instrument_long_name": "Powszechna Kasa Oszczednosci Bank Polski SA",
                "instrument_market_name": "WSE",
                "instrument_sector_name": "Financial Services",
                "instrument_industry_name": "Banks - Regional",
                "instrument_price_category": "Mid Stock",
                "yearly_price_change_category": "Neutral",
                "is_active_flag": "YES"
            }
        }

class QuoteResponse(BaseModel):
    instrument_code: str = Field(..., description="Symbol aktywa")
    quote_date: str = Field(..., description="Data sesji giełdowej (YYYY-MM-DD)")
    open_price: float = Field(..., description="Cena otwarcia sesji")
    close_price: float = Field(..., description="Cena zamknięcia sesji")
    low_price: float = Field(..., description="Najniższa cena w ciągu dnia")
    high_price: float = Field(..., description="Najwyższa cena w ciągu dnia")
    volume_number: int = Field(..., description="Wolumen obrotu na sesji")

    class Config:
        json_schema_extra = {
            "example": {
                "instrument_code": "AAPL",
                "quote_date": "2026-06-10",
                "open_price": 175.50,
                "close_price": 177.20,
                "low_price": 174.90,
                "high_price": 178.00,
                "volume_number": 52000000
            }
        }

class MacroResponse(BaseModel):
    country_code: str = Field(..., description="Kod kraju w formacie ISO Alpha-2")
    country_name: str = Field(..., description="Pełna nazwa państwa")
    indicator_code: str = Field(..., description="Kod wskaźnika w systemie FRED")
    indicator_name: str = Field(..., description="Nazwa wewnętrzna wskaźnika makro")
    declaration_date: str = Field(..., description="Data odczytu danych (YYYY-MM-DD)")
    indicator_value: float = Field(..., description="Wartość numeryczna wskaźnika")

    class Config:
        json_schema_extra = {
            "example": {
                "country_code": "PL",
                "country_name": "Poland",
                "indicator_code": "POLCPIALLMINMEI",
                "indicator_name": "PL_INFLATION",
                "declaration_date": "2026-05-01",
                "indicator_value": 4.20
            }
        }

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

@app.get("/", include_in_schema=False)
def read_root():
    """Root health-check endpoint."""
    return {
        "status": "healthy",
        "message": "Financial Data Warehouse API operational. Documentation available at /docs"
    }

@app.get(
    "/api/instruments", 
    response_model=List[InstrumentResponse], 
    tags=["Spółki i Instrumenty"],
    summary="Pobierz listę zarejestrowanych spółek"
)
def get_instruments():
    """Zwraca wszystkie instrumenty finansowe dostępne w tabeli wymiarów hurtowni (`dwh.instrument_dim`)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT instrument_id, instrument_code, 
                   COALESCE(instrument_short_name, instrument_code) AS instrument_short_name, 
                   COALESCE(instrument_long_name, instrument_code) AS instrument_long_name, 
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

@app.get(
    "/api/quotes", 
    response_model=List[QuoteResponse], 
    tags=["Notowania Giełdowe"],
    summary="Pobierz historyczne wyceny akcji"
)
def get_quotes(
    ticker: str = Query(None, description="Filtruj notowania po symbolu aktywa (np. AAPL lub PKO.WA)"),
    limit: int = Query(100, ge=1, le=1000, description="Maksymalna liczba zwracanych wierszy danych")
):
    """Zwraca historyczne fakty giełdowe z tabeli `dwh.quote_fact` powiązane z wymiarami czasu i instrumentów."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT i.instrument_code, d.date::text as quote_date, 
                   q.open_price::numeric as open_price, q.close_price::numeric as close_price, 
                   q.low_price::numeric as low_price, q.high_price::numeric as high_price, 
                   q.volume_number
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
        result = cursor.fetchall()
        return result if result is not None else []
    except Exception as e:
        logger.error(f"Error querying dwh.quote_fact: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stock quotes data")
    finally:
        cursor.close()
        conn.close()

@app.get(
    "/api/macro", 
    response_model=List[MacroResponse], 
    tags=["Wskaźniki Makroekonomiczne"],
    summary="Pobierz surowe indeksy FRED"
)
def get_macro_data(
    country_code: str = Query(None, description="Filtruj wskaźniki po kodzie kraju (np. US, PL)"),
    limit: int = Query(200, ge=1, le=2000, description="Maksymalna liczba zwracanych wierszy danych")
):
    """Zwraca dane makroekonomiczne (PKB, Inflacja, Bezrobocie) zsynchronizowane z serwerów bazy FRED."""
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