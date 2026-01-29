# 1. Base Python image (lightweight version)
FROM python:3.9-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy dependencies file and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application code
COPY . .

# 5. Expose port 5000 to the outside world
EXPOSE 5000

# 6. Start the application using Gunicorn (Production Server)
# --bind 0.0.0.0:5000 : Listen on all available network interfaces on port 5000
# run:app             : Look for 'app' object in 'run.py' file
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]