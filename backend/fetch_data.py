import requests
import pandas as pd
from datetime import timedelta

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets"

def fetch_actuals(start_date: str, end_date: str) -> pd.DataFrame:
    print(f"Fetching actuals from {start_date} to {end_date} in 7-day chunks...")
    current_start = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    all_data = []
    
    while current_start <= end_dt:
        current_end = min(current_start + timedelta(days=6), end_dt)
        
        s_str = current_start.strftime("%Y-%m-%d")
        e_str = current_end.strftime("%Y-%m-%d")
        print(f"  -> Fetching actuals: {s_str} to {e_str}")
        
        url = f"{BASE_URL}/FUELHH?settlementDateFrom={s_str}&settlementDateTo={e_str}&format=json"
        response = requests.get(url)
        response.raise_for_status()
        
        all_data.extend(response.json().get('data', []))
        current_start = current_end + timedelta(days=1)
        
    df = pd.DataFrame(all_data)
    df = df[df['fuelType'] == 'WIND'].copy()
    df = df[['startTime', 'generation']]
    df.rename(columns={'generation': 'actual_generation'}, inplace=True)
    df['startTime'] = pd.to_datetime(df['startTime'])
    return df

def fetch_forecasts(start_date: str, end_date: str) -> pd.DataFrame:
    print(f"Fetching forecasts from {start_date} to {end_date} in 7-day chunks...")
    current_start = pd.to_datetime(start_date) - timedelta(days=1) 
    end_dt = pd.to_datetime(end_date)
    
    all_data = []
    
    while current_start <= end_dt:
        current_end = min(current_start + timedelta(days=6), end_dt)
        
        s_str = current_start.strftime("%Y-%m-%dT00:00:00Z")
        e_str = current_end.strftime("%Y-%m-%dT23:59:59Z")
        print(f"  -> Fetching forecasts: {s_str} to {e_str}")
        
        url = f"{BASE_URL}/WINDFOR?publishDateTimeFrom={s_str}&publishDateTimeTo={e_str}&format=json"
        response = requests.get(url)
        response.raise_for_status()
        
        all_data.extend(response.json().get('data', []))
        current_start = current_end + timedelta(days=1)
        
    df = pd.DataFrame(all_data)
    df = df[['publishTime', 'startTime', 'generation']]
    df.rename(columns={'generation': 'forecast_generation'}, inplace=True)
    
    df['publishTime'] = pd.to_datetime(df['publishTime'])
    df['startTime'] = pd.to_datetime(df['startTime'])
    
    df['delivery_date'] = df['startTime'].dt.floor('D')
    valid_forecasts = df[df['publishTime'] < df['delivery_date']].copy()
    
    valid_forecasts = valid_forecasts.sort_values('publishTime', ascending=False)
    best_forecasts = valid_forecasts.drop_duplicates(subset=['startTime'], keep='first')
    
    best_forecasts = best_forecasts[
        (best_forecasts['startTime'] >= pd.to_datetime("2026-01-01T00:00:00Z")) & 
        (best_forecasts['startTime'] <= pd.to_datetime("2026-01-31T23:30:00Z"))
    ]
    
    return best_forecasts[['startTime', 'forecast_generation']]

def main():
    start_date = "2026-01-01"
    end_date = "2026-01-31"
    
    actuals_df = fetch_actuals(start_date, end_date)
    forecasts_df = fetch_forecasts(start_date, end_date)
    
    print("Merging datasets...")
    merged_df = pd.merge(actuals_df, forecasts_df, on='startTime', how='inner')
    merged_df = merged_df.sort_values('startTime')
    merged_df.dropna(inplace=True)
    
    output_file = "jan_2026_wind_data.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"Success! Saved {len(merged_df)} records to '{output_file}'.")

if __name__ == "__main__":
    main()