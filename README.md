# Data Ingestion API

This repo implements a basic API using Pydantic and FastAPI to ingest
data stored in CSVs.
The example data consists on hyphotetical employee records
from a certain company organized under three
tables: employees, deparments and jobs.

## Requirements

All the requirements are stored on the requirements.txt file.
We highly encourage you to use some kind of virtualenv for your development
work. Use the one you prefer and run:

```
pip install -r requirements.txt
```

## Precommit

This repo contains a basic pre-commit file to automatically check the syntax
and style of your work. To install it simply run:

```
pre-commit install
```


## Usage

Execute the initial migrations by running:

```
alembic upgrade head
```

Start the server by running:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

You can use the /docs endpoint to quickly test the API.
