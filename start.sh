#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn process.
exec gunicorn stackbuilders__test.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3