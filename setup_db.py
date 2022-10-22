import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = environ.Env()
ENV.read_env(os.path.join(BASE_DIR, ".env"))

pg_host = ENV.str("POSTGRES_HOST")
pg_user = ENV.str("POSTGRES_ROOT_USER")
pg_password = ENV.str("POSTGRES_ROOT_PASSWORD")
pg_root_db = ENV.str("POSTGRES_ROOT_NAME")

con = psycopg2.connect(
    "host={} user={} password='{}' dbname={}".format(
        pg_host, pg_user, pg_password, pg_root_db
    )
)
app_Database = ENV.str("POSTGRES_DB")
app_user = ENV.str("POSTGRES_USER")
app_user_password = ENV.str("POSTGRES_PASSWORD")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = con.cursor()

sqlCheckDatabase = "SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('{}');".format(
    app_Database
)
sqlCreateDatabase = "create database {};".format(app_Database)
sqlCreateUser = "CREATE USER {} WITH PASSWORD '{}' CREATEDB;".format(app_user, app_user_password)
sqlCheckUser = "SELECT 1 FROM pg_roles WHERE rolname='{}'".format(app_user)

sqlGrantQuery =  """
ALTER ROLE {0} SET client_encoding TO 'utf8';
ALTER ROLE {0} SET default_transaction_isolation TO 'read committed';
ALTER ROLE {0} SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE {1} TO {0};
""".format(app_user, app_Database)


# Create DB
cursor.execute(sqlCheckDatabase)
if cursor.fetchone() is None:
    cursor.execute(sqlCreateDatabase)

# Create Role
cursor.execute(sqlCheckUser)
if cursor.fetchone() is None:
    cursor.execute(sqlCreateUser)
cursor.execute(sqlGrantQuery)
