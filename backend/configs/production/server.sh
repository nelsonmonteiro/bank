#!/bin/bash

set -e
LOGFILE=/home/ubuntu/sites/bank/logs/nmonteiro_gunicorn.access.log
ERRORFILE=/home/ubuntu/sites/bank/logs/nmonteiro_gunicorn.error.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
TIMEOUT=120

#The below address:port info will be used later to configure Nginx with Gunicorn
ADDRESS=unix:/var/run/nmonteiro.sock

cd /home/ubuntu/sites/bank/backend
source ./env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/ubuntu/sites/bank/backend
test -d $LOGDIR || mkdir -p $LOGDIR
exec ./env/bin/gunicorn nmonteiro.configs.production.wsgi:application -w $NUM_WORKERS --bind=$ADDRESS \
--log-level=DEBUG --log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE --timeout $TIMEOUT
