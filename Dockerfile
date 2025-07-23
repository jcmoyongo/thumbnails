# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

#Make sure the directory exists inside the container. This is one option. Another other is to use a volume in docker-compose.yml or do it in the Python code.
# This is where the thumbnails will be saved
RUN mkdir -p /app/thumb_nails

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# Assuming you're inside your Dockerfile before switching users
RUN chown -R appuser:appuser /app


USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["python", "thumb_nails.py"]
CMD ["sh", "-c", "python thumb_nails.py && sleep 3600"]

