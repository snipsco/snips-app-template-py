#!/usr/bin/env bash
set -e

if [ ! -e "./config.ini" ]; then
    cp config.ini.default config.ini
fi

VENV=venv

if [ ! -d "$VENV" ]; then
    PYTHON=`which python3`

    if [ -f "$PYTHON" ]
    then
        echo "could not find python3"
    fi
    virtualenv -p $PYTHON $VENV
fi

. $VENV/bin/activate

pip3 install -r requirements.txt
