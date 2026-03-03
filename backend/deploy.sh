#!/bin/bash

# Exit on any error
set -e

echo "Starting deployment process..."

# 1. Pull the latest code from GitHub/GitLab
echo "Pulling latest code..."
git pull origin main

# 2. Activate the virtual environment
# Update this path if your venv is located somewhere else (e.g., ~/.virtualenvs/xtn)
source venv/bin/activate

# 3. Install/Update required dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# 4. Collect static files
# Gathers all CSS/JS/Images into the /staticfiles/ directory for Nginx to serve
echo "Gathering static files..."
python manage.py collectstatic --noinput

# 5. Run database migrations
# Applies any model changes to the live PostgreSQL database
echo "Running database migrations..."
python manage.py migrate

# 6. Restart the Gunicorn Application Server
# Assumes you have set up a systemd service named 'gunicorn' or 'xtn-api'
echo "Restarting application server..."
# sudo systemctl restart gunicorn
# (Uncomment and replace 'gunicorn' with your actual service name when ready)

echo "Deployment completed successfully! ✅"
