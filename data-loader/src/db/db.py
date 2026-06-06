import logging
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text


logger = logging.getLogger(__name__)

def ensure_table(conn, table_name, df, primary_keys):
    try:
        df.head(0).to_sql(
            name=table_name,
            con=conn,
            schema='raw',
            if_exists='fail',
            index=False,
        )
    except ValueError as e:
        # Do not touch this code unless you know exactly what you are doing.
        # This is not a standard way of checking if a table exists, but it works.
        # Table already exists, there is no need to alter it.
        return
    except Exception as e:
        logger.critical(f'Error creating table raw.{table_name}: {e}')
        raise

    constraint_name = f'{table_name}_PK'
    cols = ', '.join(primary_keys)
    conn.execute(text(f"""
        ALTER TABLE raw.{table_name}
        ADD CONSTRAINT {constraint_name} PRIMARY KEY ({cols})
    """))

def ensure_timestamps_table(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS raw._timestamps (
            table_name  TEXT        PRIMARY KEY,
            loaded_at   TIMESTAMPTZ NOT NULL
        )
    """))


def get_timestamp(conn, table_name):
    row = conn.execute(
        text('SELECT loaded_at FROM raw._timestamps WHERE table_name = :t'),
        {'t': table_name},
    ).fetchone()
    return row[0] if row else None


def set_timestamp(conn, table_name, loaded_at):
    conn.execute(text("""
        INSERT INTO raw._timestamps (table_name, loaded_at)
        VALUES (:t, :ts)
        ON CONFLICT (table_name)
        DO UPDATE SET loaded_at = EXCLUDED.loaded_at
    """), {'t': table_name, 'ts': loaded_at})


def upsert(conn, table_name, df, primary_keys):
    pk_nulls = df[primary_keys].isnull().any(axis=1)
    if pk_nulls.any():
        null_count = pk_nulls.sum()
        logger.warning(f'{null_count} rows have null values in primary keys {primary_keys} and will be skipped')
    df = df.dropna(subset=primary_keys)
    try:
        df.to_sql(
            name=table_name,
            con=conn,
            schema='raw',
            if_exists='append',
            index=False,
            method=_upsert_method(primary_keys),
            chunksize=100,
        )
    except Exception as e:
        logger.critical(f'Error upserting data to raw.{table_name}: {e}')
        raise

def _upsert_method(primary_keys):
    def method(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        if not data:
            return

        insert_stmt = insert(table.table).values(data)

        update_dict = {
            c.name: c
            for c in insert_stmt.excluded
            if c.name not in primary_keys
        }

        if update_dict:
            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=primary_keys,
                set_=update_dict,
            )
        else:
            upsert_stmt = insert_stmt.on_conflict_do_nothing(
                index_elements=primary_keys,
            )

        conn.execute(upsert_stmt.execution_options(render_postcompile=True))

    return method