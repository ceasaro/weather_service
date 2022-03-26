#!/bin/bash

if [ $# -lt 2 ]; then
  echo "$0 <name> <prefixpath>" # e.g. development /opt/cropx
  exit 1
fi

export HOME="/home/cropx"
export USER=cropx
export PGHOST=postgis

NAME=$1                                         # Name of the application
DJANGODIR="$2/api"                              # Django project directory
SOCKFILE="/var/tmp/gunicorn.sock"               # we will communicate using this unix socket
PIDFILE="/var/tmp/gunicorn.pid"
NUM_WORKERS=5                                   # how many worker processes should Gunicorn spawn = 2*numcpu + 1
DJANGO_SETTINGS_MODULE=weather_service.settings          # which settings file should Django use
DJANGO_ASGI_MODULE=weather_service.asgi                  # WSGI module name

echo "Starting $NAME"

cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/cropx/env/bin/gunicorn ${DJANGO_ASGI_MODULE}:application \
  -k uvicorn.workers.UvicornWorker \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=cropx --group=cropx \
  --timeout=120 --graceful-timeout=10 \
  --log-level=debug \
  --pid $PIDFILE \
  --limit-request-line=0 \
  --bind=unix:$SOCKFILE
