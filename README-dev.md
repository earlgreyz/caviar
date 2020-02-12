# Setting up the development environment

Before proceeding follow the guide in [README](./README.md) to set up the
virtual environment. Make sure you have it activated before installing
additional packages.
```sh
$ source venv/bin/activate
```

## Installing required python packages
```sh
(venv) $ pip install -r requirements-dev.txt
```

## Installing pre-commit hooks
```sh
(venv) $ pre-commit install
```
