# Weather Data Pipeline

ETL pipeline for fetching and processing weather data from OpenWeatherMap API.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-green.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-17%20passing-success.svg)](tests/)

---

## Features

- Fetches weather data for multiple cities
- Transforms data (Kelvin to Celsius, Unix timestamps)
- PostgreSQL storage with proper schema design
- Production-quality logging and error handling
- Comprehensive test suite (17 unit tests with mocking)
- Fully Dockerized - runs with single command


---

## Project structure
```
├── src/
│   ├── extract/      # API client, handles HTTP requests
│   ├── transform/    # Data cleaning (Kelvin→Celsius, timestamps)
│   ├── load/         # Database operations
│   └── utils/        # Logging setup
├── tests/            # Unit tests with pytest
├── config/           # Configuration (cities list, API settings)
├── sql/              # Database schema
└── docker-compose.yml
```

**Tech used**

- Python 3.11
- PostgreSQL 18
- Docker
- pytest (testing)
- psycopg2 (database connection)

---

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- OpenWeatherMap API key ([get free key](https://openweathermap.org/api))

### Installation

1. **Clone repository**
```bash
git clone https://github.com/Tensiorr/Weather_data_pipeline.git
cd weather-data-pipeline
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your OPENWEATHER_API_KEY
```

3. **Run with Docker**
```bash
docker-compose up
```

That's it! The pipeline will:
- ✅ Start PostgreSQL database
- ✅ Create tables automatically
- ✅ Fetch weather data for configured cities
- ✅ Store data with duplicate detection

---
