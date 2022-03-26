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
Note: sometimes makemigrations fails to detect application migrations
in that case run this command ```python manage.py makemigrations forceartsapi```
before running ```python manage.py migrate``` command.

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
        'NAME': 'database',
    }
}
```

### Seed database
Populate the database with fixtures: 
```
python manage.py loaddata data.json
```
Optional: You could also create your own data.json file but 
don't forget to convert data.json file to UTF-8 format: 
```
python -Xutf8 manage.py dumpdata > data.json
```

###Unit Tests
We have included several unit tests that checks ```urls.py```, ```models.py```,
```views.py```, ```commands.py```, and etc. You can run unit tests by entering
this command ```python manage.py test``` in your terminal. This command will trigger
all tests inside ```tests``` folder.

### Endpoints:
``` 
1. [GET] http://127.0.0.1:8000/api/category
2. [GET] http://127.0.0.1:8000/api/search?limit=20&offset=0&query=&order=likes
3. [POST] http://127.0.0.1:8000/api/user/create/
4. [POST] http://127.0.0.1:8000/api/user/auth/
5. [GET] http://127.0.0.1:8000/api/user/me/
6. [PATCH] http://127.0.0.1:8000/api/user/me/
7. [POST] http://127.0.0.1:8000/api/wallpaper/
8. [GET] http://127.0.0.1:8000/api/wallpaper/<wallpaper_id>/
9. [PUT] http://127.0.0.1:8000/api/wallpaper/<wallpaper_id>/
10. [PATCH] http://127.0.0.1:8000/api/wallpaper/<wallpaper_id>/
11. [DELETE] http://127.0.0.1:8000/api/wallpaper/<wallpaper_id>/
12. [POST] http://127.0.0.1:8000/api/contact-us
```
