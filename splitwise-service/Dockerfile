FROM python:3.8-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /tmp/

# COPY ./packages /tmp/packages

RUN poetry export --output requirements.txt --without-hashes

FROM python:3.8-slim

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# COPY ./packages /tmp/packages

RUN apt update && \
    apt install -y gcc libpq-dev libpq5 && \
    pip install --no-cache-dir --upgrade -r /app/requirements.txt && \
    apt-get remove -y gcc libpq-dev && apt-get -y autoremove

COPY ./src /app/src
COPY ./build_info.json /app/
COPY ./alembic.prod.ini /app/alembic.ini
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
