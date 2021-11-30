if [ -f "./Pipfile" ]
then
    pipenv run pytest -rP -v --cov="$(pwd)" --cov-report html
else
    if [ -d "./venv" ]
    then
        source ./venv/bin/activate
    fi
    pytest -rP -v --cov="$(pwd)" --cov-report html
fi