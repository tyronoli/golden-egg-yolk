FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

EXPOSE 8000

# Placeholder until T-002 replaces it with Django.
CMD ["python", "placeholder_server.py"]
