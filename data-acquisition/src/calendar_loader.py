from datetime import datetime
import pandas as pd
import pandas_market_calendars as mcal
import exchange_calendars as xcal

def get_trading_calendars(start_date = '2020-01-01', end_date = '2026-12-31'):
    end_date_year = datetime.strptime(end_date, '%Y-%m-%d').year
    current_year = datetime.now().year
    if end_date_year > current_year:
        raise ValueError(f'End date year: {end_date_year} cannot be greater than current year: {current_year}. Cannot fetch future calendar for wse.')

    dates = pd.date_range(start=start_date, end=end_date)
    df = pd.DataFrame(index=dates)
    
    nyse = mcal.get_calendar('NYSE')
    nyse_schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    wse = xcal.get_calendar("XWAR")
    wse_schedule = wse.sessions_in_range(start_date, end_date)
    
    us_days = pd.to_datetime(nyse_schedule.index.date)
    us_early = pd.to_datetime(nyse.early_closes(nyse_schedule).index.date)
    wse_days = pd.to_datetime(wse_schedule.date)
    
    df['is_us_trading_day'] = df.index.isin(us_days)
    df['is_us_early_close'] = df.index.isin(us_early)
    df['is_pl_trading_day'] = df.index.isin(wse_days)
    
    return df.reset_index().rename(columns={'index': 'date'})
