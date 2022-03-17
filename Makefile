deleteDB:
	rm db.sqlite3 apps/*/migrations/0*
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
