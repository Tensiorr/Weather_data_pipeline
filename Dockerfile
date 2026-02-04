FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY config/ /app/config/
COPY sql/ /app/sql/

ENV PYTHONPATH=/app/src
CMD ["python", "-m", "src.pipeline"]