import sqlalchemy as sa

from config import config
 
 
def build_engine():
    url = sa.URL.create(
        drivername='postgresql+psycopg',
        host=config.POSTGRES_HOST,
        port=5432,
        database=config.POSTGRES_DB,
        username=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
    )
    return sa.create_engine(url, pool_pre_ping=True)
