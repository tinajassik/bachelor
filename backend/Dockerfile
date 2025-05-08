# Use a Python version compatible with your pyproject.toml (>=3.11)
# You can try being more specific, e.g., python:3.11.9-slim if that's the latest patch
FROM python:3.11-slim

# Update OS packages to try and mitigate known vulnerabilities
# and install dependencies for OpenCV (cv2)
RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Set essential environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.8.3

# Install Poetry
RUN pip install "poetry==${POETRY_VERSION}"

# Set the working directory in the container
WORKDIR /app

# Copy only the dependency definition files first to leverage Docker cache
# It's crucial that poetry.lock is committed to your repository.
COPY pyproject.toml poetry.lock* ./

# Install project dependencies using Poetry
# --no-dev: Excludes development dependencies (like ipykernel from your dev group)
# --no-interaction: Prevents Poetry from asking interactive questions
# --no-ansi: Cleaner logs
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy your main application file
COPY main.py ./

# Copy the 'src' directory if it contains other modules your main.py might use
COPY src/ ./src/

# Create the 'static' directory as the application expects it, even if it's empty
RUN mkdir -p /app/static

# Explicitly set PYTHONPATH to include /app (where main.py is)
# and /app/src (where other packages like api_routes are)
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/src"

# If you have other necessary files/directories at the root of your backend project (e.g. config files), copy them too.
# Example: COPY config.yaml .

# Make port 8000 available to the world outside this container (adjust if your Python app uses a different port)
EXPOSE 8000

# Command to run your FastAPI application using Uvicorn, managed by Poetry
# Assumes your main FastAPI file is main.py (at /app/main.py in the container)
# and the FastAPI instance is named 'app'.
# Added --reload for development.
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--app-dir", "/app"]
