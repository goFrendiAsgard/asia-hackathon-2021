if [ -f "./Pipfile" ]
then
    pipenv run ./start.sh
else
    if [ -d "./venv" ]
    then
        source ./venv/bin/activate
    fi
    ./start.sh
fi