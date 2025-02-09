# FourChan Web Archive

FourChan Web Archive is a Django-based web application designed to archive threads from 4chan. The application stores thread data and images in a PostgreSQL database and MinIO object storage, respectively. It also provides a web interface for browsing and managing the archived threads.

## Table of Contents

- Features
- [Project Structure](#project-structure)
- Installation
- Usage
- Configuration
- Contributing
- License

## Features

- Archive threads from 4chan, including images and metadata.
- Store images in MinIO object storage.
- Store thread data in a PostgreSQL database.
- Browse and manage archived threads through a web interface.
- User authentication and authorization for managing archives.

## Project Structure

```
.gitignore
db.sqlite3
docker-compose.override.yaml
docker-compose.yaml
Dockerfile
FourChanWebArchive/
minio_data/
    .minio.sys/
        buckets/
        config/
        format.json
        multipart/
        tmp/
    picels/
    tts-audio/
README.md
requirements.txt
threadark/
    db.sqlite3
    manage.py
    static/
        css/
        js/
    staticfiles/
        admin/
        CACHE/
        css/
        js/
    threadark/
        __init__.py
        __pycache__/
        asgi.py
        settings.py
        urls.py
        wsgi.py
    webarchive/
        __init__.py
        __pycache__/
        admin.py
        apps.py
        classes/
        ...
```

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/FourChanWebArchive.git
   cd FourChanWebArchive
   ```

2. Build and start the Docker containers:

   ```sh
   docker-compose up --build
   ```

3. The application will be available at [`http://localhost:8000`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fwebarchive%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A2%2C%22character%22%3A12%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition").

## Usage

### Accessing the Web Interface

Open your web browser and navigate to [`http://localhost:8000`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fwebarchive%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A2%2C%22character%22%3A12%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"). You will see the web interface for browsing and managing archived threads.

### Archiving Threads

To archive a thread, use the provided web interface to input the thread URL and start the archiving process. The application will download the thread data and images, storing them in the PostgreSQL database and MinIO object storage, respectively.

## Configuration

### Environment Variables

The application uses the following environment variables for configuration:

- [`AWS_ACCESS_KEY_ID`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fthreadark%2Fsettings.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A148%2C%22character%22%3A0%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fwebarchive%2Fclasses%2FThreadStorage.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A71%2C%22character%22%3A38%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"): Access key for MinIO.
- [`AWS_SECRET_ACCESS_KEY`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fthreadark%2Fsettings.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A149%2C%22character%22%3A0%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fwebarchive%2Fclasses%2FThreadStorage.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A72%2C%22character%22%3A38%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"): Secret key for MinIO.
- [`AWS_STORAGE_BUCKET_NAME`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fthreadark%2Fsettings.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A150%2C%22character%22%3A0%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fwebarchive%2Fclasses%2FThreadStorage.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A76%2C%22character%22%3A37%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"): Name of the MinIO bucket.
- [`AWS_S3_ENDPOINT_URL`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fthreadark%2Fsettings.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A151%2C%22character%22%3A0%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"): Endpoint URL for MinIO.
- [`DB_NAME`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fthreadark%2Fsettings.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A58%2C%22character%22%3A27%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"): Name of the PostgreSQL database.
- [`DB_USER`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fthreadark%2Fsettings.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A59%2C%22character%22%3A27%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"): Username for the PostgreSQL database.
- [`DB_PASSWORD`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fthreadark%2Fsettings.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A60%2C%22character%22%3A31%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"): Password for the PostgreSQL database.
- [`DB_HOST`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fdaniel%2Fcode%2Fprojects%2FFourChanWebArchive%2Fthreadark%2Fthreadark%2Fsettings.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A61%2C%22character%22%3A27%7D%7D%5D%2C%22d0a3e58c-95f4-44b2-aa4a-4785127891e4%22%5D "Go to definition"): Hostname for the PostgreSQL database.

### Django Settings

The Django settings are configured in 

settings.py

. You can modify this file to change the application settings, such as database configuration, static files, and media files.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to your fork.
4. Create a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.