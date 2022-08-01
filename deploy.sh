#!/bin/bash

if $ENV_FILE; then
  source "$ENV_FILE"
fi

# Create venv if does not exists
if [ ! -d "$VENV_DIRECTORY" ]; then
  virtualenv "$VENV_DIRECTORY"
  "$VENV_DIRECTORY"bin/pip install uwsgi
fi

# Remove previous deployment
rm "$APP_DIRECTORY" -rf

# Copy data
mkdir -p "$APP_DIRECTORY"
cp -r * "$APP_DIRECTORY"
cd "$APP_DIRECTORY" || exit

# Install requirements in venv
source "$VENV_DIRECTORY"bin/activate
pip install -r api/requirements.txt

# Run Django migrations
"$VENV_DIRECTORY"bin/python3 api/manage.py migrate

# Collect Django static files
"$VENV_DIRECTORY"bin/python3 api/manage.py collectstatic

# UWSGI
# Get PID file path
UWSGI_PID_FILE=$(awk -F "=" '/pidfile/ {print $2}' "$UWSGI_INI")

# reload or start application server (uwsgi)
if "$VENV_DIRECTORY"bin/uwsgi --reload "$UWSGI_PID_FILE"; then
  echo "Server reloaded"
else
  "$VENV_DIRECTORY"bin/uwsgi --ini "$UWSGI_INI"
  echo "Server started"
fi
