# UK Wind Generation Forecast Dashboard

## Overview
This application provides a dashboard for day-ahead market traders to evaluate the accuracy of UK wind generation forecasts (January 2026) using data from the Elexon API.

## File & Directory Structure
- `/backend`: Contains the FastAPI Python application.
  - `fetch_data.py`: Script to extract, clean, and merge Elexon API data into a CSV.
  - `main.py`: FastAPI server serving the time-series data and calculated error metrics (MAE, RMSE, MAPE).
  - `Dockerfile`: Container configuration for the Python environment.
- `/frontend`: Contains the React/Vite dashboard application.
  - `src/App.tsx`: Main React component containing the Recharts graph and UI logic.
  - `Dockerfile`: Multi-stage build using Nginx to serve the React application.
- `docker-compose.yml`: Orchestrates both frontend and backend services.

## How to Start Locally
Make sure you have Docker Desktop installed and running.
1. Clone this repository.
2. Open a terminal in the root directory.
3. Run the following command:
   ```bash
   docker-compose up --build
Access the frontend dashboard at http://localhost:3000.

Access the backend API at http://localhost:8000.

Live Deployment Links
Frontend (Vercel): [INSERT_VERCEL_LINK_HERE]

Backend (Heroku): [INSERT_HEROKU_LINK_HERE]

AI Tools Used
AI tools (ChatGPT/Gemini) were used to assist in generating boilerplate Pandas logic for data merging, configuring the Dockerfiles, and scaffolding the React components.