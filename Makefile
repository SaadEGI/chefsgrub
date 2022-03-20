deleteDB:
	rm db.sqlite3 apps/*/migrations/0*
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
venv:
	python3 -m venv venv
	. venv/bin/activate
	pip3 install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
updateDependencies:
	pip3 freeze > requirements.txt
createSuperUser:
	python3 manage.py createsuperuser --username superuser --email sufian5@live.com --noinput
	# https://www.oreilly.com/library/view/managing-projects-with/0596006101/ch07.html