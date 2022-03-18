deleteDB:
	rm db.sqlite3 apps/*/migrations/0*
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
venv:
	virtualenv venv
	pip3 install -r requirements.txt
	source venv/bin/activate
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py runserver
updateDependencies:
	pip3 freeze > requirements.txt
createSuperUser:
	python3 manage.py createsuperuser --username superuser --email sufian5@live.com --noinput