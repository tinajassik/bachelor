# Poetry Commands Guide

Poetry is a dependency management and packaging tool for Python projects. Below is a list of commonly used commands in a Poetry-based project, along with their explanations.

## 📌 Installation

To install Poetry globally:
```sh
curl -sSL https://install.python-poetry.org | python3 -
```
Or using pip:
```sh
pip install poetry
```

## 📦 Project Initialization

To create a new Poetry project:
```sh
poetry new my_project
```
To create a project in the current directory:
```sh
poetry init
```

## 📂 Managing Dependencies

### Add a Dependency
To add a package to your project:
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

## 🏃 Running and Managing the Virtual Environment

### Activate the Virtual Environment
```sh
poetry shell
```
To exit the shell:
```sh
exit
```

### Run a Command Inside the Virtual Environment
```sh
poetry run python script.py
```

## 🔄 Dependency Management

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

## 🚀 Build 

### Build the Package
```sh
poetry build
```

## 🛠 Miscellaneous Commands

### Check for Issues
Check for dependency conflicts:
```sh
poetry check
```

### Lock the Dependencies
Generate or update `poetry.lock`:
```sh
poetry lock
```

### Export Dependencies to Requirements File
```sh
poetry export -f requirements.txt --output requirements.txt
```

## 🎯 Conclusion
Poetry simplifies dependency management and packaging in Python. These commands will help you navigate and manage a Poetry-based project efficiently!
