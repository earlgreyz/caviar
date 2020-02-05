# Setting up the development environment

## Creating the virtual environment
```sh
$ virtualenv --python=python3.7 venv
$ source venv/bin/activate
```

## Installing required python packages
```sh
(venv) $ pip install -r requirements.txt
(venv) $ pip install -r requirements-dev.txt
```

## Installing pre-commit hooks
```sh
(venv) $ pre-commit install
```
