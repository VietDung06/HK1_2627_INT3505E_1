from .src import (create_app)

app = create_app()

# gunicorn -c gunicorn.conf.py wsgi:app
# GUNICORN VIA TERMINAL NOT INTENDED TO USE ON WINDOW, AS THERE IS NO MODULE NAMED 'fcntl'
# HAS TO CONTAIN VIA DOCKER FIRST