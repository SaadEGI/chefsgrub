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
server:
	python3 -m venv venv
	. venv/bin/activate
	pip3 install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py collectstatic --no-input
	# gunicorn --bind 0.0.0.0:8800 interiorshop.wsgi:application
	sudo systemctl restart nginx 
	sudo /etc/init.d/nginx restart