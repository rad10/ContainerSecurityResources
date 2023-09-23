# syntax=docker/dockerfile:1
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-alpine

# Exposing port
EXPOSE 8000/tcp

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Creating environment variables
ENV OCTOPRINT_URL=http://0.0.0.0:80
ENV OCTOPRINT_APIKEY=ABCD1234

# Installing required libraries
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# The directory for our code will be in /app
WORKDIR /app
COPY --chown=0:5678 . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser
USER appuser

# Mounting spaces with data we prefer to keep
VOLUME [ "/app/data", "/app/uploads" ]

# Healthcheck to ensure that application is available to access
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "wget http://localhost:8000/ || exit 1" ]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
