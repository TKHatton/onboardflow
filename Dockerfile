FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install -e .

# Expose port
ENV PORT 8080
EXPOSE 8080

# Run the application
CMD ["python", "-m", "onboardflow.server"]
