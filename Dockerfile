# Base image with Python 3.9 or newer
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application script
COPY apptelebot.py /app/

# Run the application
CMD ["python", "apptelebot.py"]
