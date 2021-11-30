if [ -f "./Pipfile" ]
then
    pipenv run echo "migrate asiaApp"
else
    if [ -d "./venv" ]
    then
        source ./venv/bin/activate
    fi
    echo "migrate asiaApp"
fi