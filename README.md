# Connected Autonomic Vehicles Simulator
![unittest](https://github.com/earlgreyz/caviar/workflows/unittest/badge.svg)
[![codecov](https://codecov.io/gh/earlgreyz/caviar/branch/master/graph/badge.svg?token=8CCDT357DL)](https://codecov.io/gh/earlgreyz/caviar)

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
The simulation can be run through the `main.py` script in the
`src/` directory of this project.
```sh
(venv) $ python src/main.py
```

To see the list of all possible parameters to change use `--help`.
```sh
(venv) $ python src/main.py --help
```

The simulation parameters can also be loaded from a yaml configuration file
```sh
(venv) $ python src/main.py --config config.yaml
```

```yaml
# config.yaml
simulation:
  length: 150
  lanes: 3
  max-speed: 7
  obstacles:
    - "0:0-10"
    - "2:0-10"
  dispatch: 1
```

### Example usage
Simulation can run in two different modes:
* `gui` displaying animation of the vehicles
* `cli` running for a specific number of cycles and showing only statistics

#### GUI
You can see `gui` specific parameters by running
```sh
(venv) $ python src/main.py gui --help
```

For example to change the animation time of a single step to 200ms
```sh
(venv) $ python src/main.py gui --step 200
```

#### CLI
You can see `cli` specific parameters by running
```sh
(venv) $ python src/main.py cli --help
```

For example to change the number of steps to 1000
```sh
(venv) $ python src/main.py cli --steps 1000
```
