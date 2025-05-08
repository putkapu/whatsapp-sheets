venv:
	python3 -m venv venv

install: venv
	. venv/bin/activate && pip install -r requirements.txt

run-dev:
	FLASK_ENV=development FLASK_APP=app.py . venv/bin/activate && flask run

migrate:
	. venv/bin/activate && alembic upgrade head

clean:
	rm -rf venv __pycache__ *.pyc *.pyo whatssheet.db 

lint:
	. venv/bin/activate && flake8 src app.py

format:
	. venv/bin/activate && black src app.py

format-check:
	. venv/bin/activate && black --check src app.py

pylint:
	. venv/bin/activate && pylint src app.py 

docker-build:
	docker build -t whatssheet:latest .

docker-run:
	docker run -d --env-file .env -p $(shell grep -E '^PORT=' .env | cut -d '=' -f2):$(shell grep -E '^PORT=' .env | cut -d '=' -f2) --name whatssheet whatssheet:latest

docker-clean:
	docker stop whatssheet && docker rm whatssheet

