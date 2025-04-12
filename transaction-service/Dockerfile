# transaction-service/Dockerfile

FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5006

# Run the service
CMD ["python", "app.py"]
