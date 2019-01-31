#/usr/bin/env bash -e

if [ ! -e "./config.ini" ]
then
    cp config.ini.default config.ini
fi

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python3`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python3"
    fi
    python3 -mvenv $VENV

fi

. $VENV/bin/activate

pip3 install -r requirements.txt
