# VDJKate Database

This is a database, specifically designed to work with [VDJKate](https://github.com/valentinkelbakh/vdjk).

The project basically is a Django REST API service. 

## Installation

First clone and install requirements 


For windows
```bat
git clone https://github.com/valentinkelbakh/vdjk_db.git
cd vdjk_db
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

For Linux:
```bash
git clone https://github.com/valentinkelbakh/vdjk_db.git
cd vdjk_db
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Before start create .env file, based on .env.example.

App has webhook functionality so bot can always have latest information as soon as changes to database are made. WEBHOOK_PASS is value needed for my unique implementation of webhook. It should be some cryptographically secure random string and exactly the same string should be on .env on the bot side.


In .env.example service is set to work with MySQL Server, specifically all starting with DB_. If .env not contains DB_\* values it uses sqlite instead (eg for testing purposes)

When using MySQL, database should be created beforehand, as well as user with needed priveleges.

Example commands to execute in MySQL Console:
```sql
CREATE DATABASE db_name;
CREATE USER 'username'@'db_name' IDENTIFIED BY '123456';
GRANT ALL ON *.* TO 'username'@'db_name';
FLUSH PRIVILEGES;
```
Database name and user credentials used here should be specified in .env.

Create user, which will be used by bot to get access to the API. 
```
python manage.py createsuperuser
```
These login and password should go in bot .env file, along with WEBHOOK_PASS and url of server where this REST API service could be accessed from.

Next migrate all models to database:
```
python manage.py makemigrations
python manage.py makemigrations home
python manage.py migrate
```


To start the database:
```
python manage.py runserver
```
