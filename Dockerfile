FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
# Copy the application into the container.
COPY pyproject.toml ./pyproject.toml
RUN uv sync

COPY ./app .
RUN mkdir uploads

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "--port", "8000", "--host", "0.0.0.0"]
