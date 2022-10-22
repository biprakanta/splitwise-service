# Splitwise Service
> Splitwise Service Readme

## Usage
```
splitwise-service$ docker-compose up
```
 Go to [http://localhost:8000/docs](http://localhost:8000/docs)
## Development
### Local Environment Setup
```sh
$ sudo ./prerequisite-setup.sh
```

### Virtual environment

```sh
splitwise-service$ . ./python-setup.sh
```
This will create a virtualenv called `pyenv` in the splitwise-service folder, install all dependencies, create a `logs` folder within splitwise-service and activate the virtualenv.

**Database setup**
```bash
$ sudo -u postgres psql
CREATE DATABASE splitwisedb;
CREATE USER splitwiseuser WITH PASSWORD 'password' CREATEDB;
ALTER ROLE splitwiseuser SET client_encoding TO 'utf8';
ALTER ROLE splitwiseuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE splitwiseuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE splitwisedb TO splitwiseuser;
\q
```

For creating a superuser:
```bash
$ sudo -u postgres createuser <your-system-username> -s
```

Database access is via SQLAlchemy and uses the common Core and ORM syntax offered in v1.4/2.0. More details [here](https://docs.sqlalchemy.org/en/14/tutorial/index.html).


**Database migrations**:

Table migrations are managed via [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html). You will mostly be dealing with the following two commands:
1. Creating a new migration for the model changes:
    ```bash
    $ alembic revision --autogenerate -m "mention changes here"
    ```
    This is equivalent of Django's `makemigrations` command.
2. Running the migrations:
    ```bash
    $ alembic upgrade head
    ```
    This is the equivalent of Django's `migrate` command.

Refer to the documentation for more configurations.

### Adding dependencies
```
python -m poetry add <package-name>
python -m poetry add <package-name> --dev
```
Add `--dev ` for dev dependencies like `pytest`

### Server start watch-mode
```
python -m uvicorn src.main:app --reload --port 8080
```
### Server tests
```
python -m poetry run pytest  --asyncio-mode=auto --cov src --disable-warnings --cov-report term-missing
```


### Build and run Docker image for other development reqirements
```
docker build . -t splitwise-service
docker run -p 8000:8000 splitwise-service
```
Change the exposed port or internal port in case of conflict with other services
