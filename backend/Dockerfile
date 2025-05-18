FROM python:3.11-slim

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && apt-get upgrade -y

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.8.3

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-dev --no-interaction --no-ansi

COPY main.py ./

COPY src/ ./src/

RUN mkdir -p /app/car_detection_model
COPY car_detection_model/best.pt /app/car_detection_model/best.pt

RUN mkdir -p /app/static

ENV PYTHONPATH "${PYTHONPATH}:/app:/app/src"


EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--app-dir", "/app"]
