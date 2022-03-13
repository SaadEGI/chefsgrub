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

## Resources
### interiorshop

This repository is a part of a video tutorial on my YouTube channel: Code With Stein

### YouTube

[YouTube playlist](https://www.youtube.com/watch?v=jmc0gV6_NE0&list=PLpyspNLjzwBkeyP_4_bZBdtRjZQreDR_H)

### Website

[Code With Stein - Website](https://codewithstein.com)