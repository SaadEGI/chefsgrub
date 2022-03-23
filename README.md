# Backend-Chef
## Setup

1. Create virtual environment:
```
virtualenv venv
```
2. Install requirements:

```
pip install -r requirements.txt
```
3. Activate virutal environment:

```
source venv/bin/activate
```
4. Create DB(sqlite4):

```
python3 manage.py migrate
```
5. Run migrations:

```
python3 manage.py makemigrations 
# TODO: add snippet to do migrations to all appsdjango.db.migrations.exceptions.NodeNotFoundError
python3 manage.py migrate
```
6. Run server:

```
python3 manage.py runserver
```
7. Deactivate virutal environment:

```
deactivate
```

##Setting up POSTgres for django app

https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8

## Development

For development, [git-flow](https://gitlab.com/strtporg/backend-chef/-/wikis/Git-Flow) workflow is used
## Resources
### interiorshop

This repository is a part of a video tutorial on my YouTube channel: Code With Stein

### YouTube

[YouTube playlist](https://www.youtube.com/watch?v=jmc0gV6_NE0&list=PLpyspNLjzwBkeyP_4_bZBdtRjZQreDR_H)

### Website

[Code With Stein - Website](https://codewithstein.com)
