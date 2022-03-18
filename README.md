# Gallery-API

### Introduction
Simple wallpaper project. Django Rest Framework was used for API creation


### Used Packages
```
asgiref==3.2.10
certifi==2021.5.30
chardet==4.0.0
Django==3.1
django-appconf==1.0.4
django-cors-headers==3.7.0
django-imagekit==4.0.2
django-taggit==1.4.0
djangorestframework==3.12.4
idna==2.10
pilkit==2.0
Pillow==8.2.0
psycopg2-binary==2.8.6
pytz==2021.1
requests==2.25.1
six==1.16.0
sqlparse==0.4.1
urllib3==1.26.5
```

### Database
Normally, you should not use sqlite database in production but for testing purposes it's more than enough. If you plan 
to move into production consider using PostgreSQL or other SQL type databases. All you have to do is edit database 
section settings.py file of the project. And don't forget to install pipenv install psycopg2 in order to be able to 
connect with PostgresSQL database.

Instead of using PostgreSQL you can also use SQLite database. Please change ```settings.py``` of the project to use
SQLite database
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
```

### Setup

Note: pipenv is required, you can install it by executing this command```pip install pipenv```
```
git clone git@github.com:shukhrat121995/gallery-api.git
cd gallery-api
pipenv install
pipenv sync
pipenv shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Available routes:

1. http://127.0.0.1:8000/api/characters

2. http://127.0.0.1:8000/api/search?limit=20&offset=0&query=&order=likes







