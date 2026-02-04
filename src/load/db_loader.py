import os
import logging
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Create database connection."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def save_to_database(data: list[dict]) -> None:
    """Save weather data to PostgreSQL."""
    logger = logging.getLogger(__name__)
    if not data:
        logger.warning("No data to save")
        return

    clean_data = [record for record in data if record is not None]

    if not clean_data:
        logger.warning("No valid data to save (all records failed transformation)")
        return

    if len(clean_data) < len(data):
        logger.warning("Skipped %d invalid records", len(data) - len(clean_data))

    dbconnect = get_db_connection()
    dbconnect.autocommit = True
    cursor = dbconnect.cursor()

    sql = """
    INSERT INTO weather_measurements 
    (city, temperature_celsius, measurement_time, humidity, pressure, wind_speed)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    inserted_count = 0
    duplicate_count = 0

    for record in clean_data:
        try:
            cursor.execute(
                sql,
                (
                    record["city"],
                    record["temperature_celsius"],
                    record["measurement_time"],
                    record["humidity"],
                    record["pressure"],
                    record["wind_speed"],
                ),
            )
            inserted_count += 1
        except psycopg2.IntegrityError:
            logger.debug("Duplicated record")
            duplicate_count += 1
            continue

    cursor.close()
    dbconnect.close()
    logger.info("Inserted %d records, %d duplicates", inserted_count, duplicate_count)
