#!/bin/sh

#
# docker entrypoint script for brickwall-web docker-image
#

MODE="$@"

PROCNAME="brickwall-web"
ADDRESS="0.0.0.0:5000"
WORKERS=$(lscpu | grep ^CPU\(s\) | awk '{print $2}')

ACCESS_LOG="-"
ERROR_LOG=$ACCESS_LOG
LOG_LEVEL="INFO"

export FLASK_APPSECRETS=$(pwd)/.secrets.yml
export FLASK_APP="app"
        
flask db upgrade

if [ "$MODE" = production ]; then
        export FLASK_ENV="$MODE"
        gunicorn -b $ADDRESS -w $WORKERS -n $PROCNAME \
                --access-logfile $ACCESS_LOG \
                --error-logfile $ERROR_LOG \
                --log-level $LOG_LEVEL \
                .:app.wsgi_app
elif [ "$MODE" = testing ]; then
        export FLASK_ENV="$MODE"
        export FLASK_COVERAGE=1
        echo "To be implemented"
else
        export FLASK_ENV="development"
        flask run \
                --reload \
                -h $(echo $ADDRESS | cut -d : -f 1)
fi

