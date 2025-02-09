# Dockerfile
FROM python:3.11-slim

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Install sass
RUN npm install -g sass uglify-js cssmin
# Set the working directory
WORKDIR /app
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Start the Django server
CMD ["python", "FourChanWebArchive/manage.py", "runserver", "0.0.0.0:8000"]
