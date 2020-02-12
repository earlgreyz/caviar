# Connected Autonomic Vehicles Simulator

## Setting up the environment

To avoid package conflicts it is recommended to create a virtual environment
for the dependencies.

### Creating the virtual environment
```sh
$ virtualenv --python=python3.7 venv
$ source venv/bin/activate
```

### Installing required python packages
```sh
(venv) $ pip install -r requirements.txt
```

## Running the simulation
The simulation can be run through the `main.py` script in  the
`src/` directory of this project.
```sh
(venv) $ python src/main.py
```

To see the list of all possible parameters to change use `--help`.
```sh
(venv) $ python src/main.py --help
```

### Example usage
Change the road length to `200` and the probability of car slowing down to `0.2`.
```sh
(venv) $ python src/main.py --length 200 --pslow .2
```
