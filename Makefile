.PHONY: all upgrade debug node stage deploy scss


upgrade:
	python3 manage.py makemigrations && \
		python3 manage.py migrate

debug:
	python3 manage.py runserver

node:
	node server.js

stage:
	echo 'Not implemented'

clean_migrations:
	rm db.sqlite3
	ag -g "migrations/.*" -0 | xargs -0 rm
