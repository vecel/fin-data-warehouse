import sqlalchemy as sa


def ensure_timestamps_table(conn):
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS stg._timestamps (
            table_name  TEXT        PRIMARY KEY,
            loaded_at   TIMESTAMPTZ NOT NULL
        )
    """))


def get_timestamp(conn, table_name):
    row = conn.execute(
        sa.text('SELECT loaded_at FROM stg._timestamps WHERE table_name = :t'),
        {'t': table_name},
    ).fetchone()
    return row[0] if row else None


def set_timestamp(conn, table_name, loaded_at):
    conn.execute(sa.text("""
        INSERT INTO stg._timestamps (table_name, loaded_at)
        VALUES (:t, :ts)
        ON CONFLICT (table_name)
        DO UPDATE SET loaded_at = EXCLUDED.loaded_at
    """), {'t': table_name, 'ts': loaded_at})