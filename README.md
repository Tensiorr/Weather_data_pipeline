# Weather Data Pipeline

ETL pipeline for fetching and processing weather data from OpenWeatherMap API.

## Features
- Fetches weather data for multiple cities
- Transforms data (Kelvin to Celsius, Unix timestamps)
- Saves to CSV with error handling
- Comprehensive logging

## Setup
1. Create `.env` file with `OPENWEATHER_API_KEY=your_key`
2. Install: `pip install -r requirements.txt`
3. Run: `python src/pipeline.py`

## Project Structure
- `src/extract/` - API data fetching
- `src/transform/` - Data transformation
- `src/load/` - Data storage
- `config/` - Configuration files
- `logs/` - Application logs