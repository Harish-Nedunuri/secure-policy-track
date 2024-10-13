# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Create and set the working directory
WORKDIR /app

# Install system dependencies needed for psycopg2 and other packages
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && apt-get clean

# Copy the application files into the working directory
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
