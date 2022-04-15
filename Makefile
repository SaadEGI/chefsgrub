deleteDB:
	python3 manage.py flush --no-input
	python3 manage.py reset_db --noinput
	rm -r apps/*/migrations/0* apps/*/__pycache__ apps/*/migrations/__pycache__ interiorshop/__pycache__
migrate:
	python3 manage.py makemigrations vendor core cart product order
	python3 manage.py migrate
venv:
	python3 -m venv venv
	. venv/bin/activate
	pip3 install -r requirements.txt
	python3 manage.py makemigrations vendor core cart product order
	python3 manage.py migrate
updateDependencies:
	pip3 freeze > requirements.txt
createSuperUser:
	python3 manage.py createsuperuser --username superuser --email sufian5@live.com --noinput
run:
	python3 manage.py runserver
# i18n:
#   python3 manage.py makemessages --all -i venv --no-obsolete
# 	python3 manage.py compilemessages -l de,en,ar
# 	python3 manage.py compilemessages