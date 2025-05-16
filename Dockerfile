# Use Python 3.10 for TensorFlow 2.10+ compatibility
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files to the container
COPY . .

# Upgrade pip & install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask's default port
EXPOSE 5000

# Start your Flask app
CMD ["python", "app.py"]
