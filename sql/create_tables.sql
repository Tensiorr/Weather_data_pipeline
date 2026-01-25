-- Weather Data Pipeline - Database Schema

CREATE TABLE IF NOT EXISTS weather_measurements (
    city VARCHAR(100) NOT NULL,
    measurement_time TIMESTAMP NOT NULL,
    temperature_celsius FLOAT,
    humidity INTEGER,
    pressure INTEGER,
    wind_speed FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (city, measurement_time)
);

-- Index for querying by time
CREATE INDEX IF NOT EXISTS idx_measurement_time
ON weather_measurements(measurement_time DESC);

-- Index for querying by city
CREATE INDEX IF NOT EXISTS idx_city
ON weather_measurements(city);