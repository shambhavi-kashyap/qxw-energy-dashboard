from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os

app = FastAPI(title="UK Wind Generation Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "jan_2026_wind_data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df['error'] = df['actual_generation'] - df['forecast_generation']
else:
    df = pd.DataFrame()

@app.get("/")
def root():
    return {"message": "API is running. Access /api/timeseries or /api/metrics"}

@app.get("/api/metrics")
def get_metrics():
    if df.empty:
        return {"error": "Data file not found."}
    
    mae = df['error'].abs().mean()
    
    rmse = np.sqrt((df['error'] ** 2).mean())
    
    valid_mape_df = df[df['actual_generation'] > 0]
    mape = (valid_mape_df['error'].abs() / valid_mape_df['actual_generation']).mean() * 100

    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2)
    }

@app.get("/api/timeseries")
def get_timeseries():
    if df.empty:
        return {"error": "Data file not found."}
    
    records = df[['startTime', 'actual_generation', 'forecast_generation']].to_dict(orient="records")
    return records