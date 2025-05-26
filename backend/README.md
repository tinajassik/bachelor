## Managing Dependencies

### Add a Dependency
To add a package to project:
```sh
poetry add package_name
```
To add a development dependency:
```sh
poetry add --dev package_name
```

### Remove a Dependency
```sh
poetry remove package_name
```

### Install Dependencies
Installs dependencies from `pyproject.toml`:
```sh
poetry install
```

### Run a Command Inside the Virtual Environment
```sh
poetry run python main.py
```

### Update Dependencies
Update all dependencies:
```sh
poetry update
```
Update a specific package:
```sh
poetry update package_name
```

### Show Installed Dependencies
```sh
poetry show
```

### Lock the Dependencies
Generate or update `poetry.lock`:
```sh
poetry lock
```
