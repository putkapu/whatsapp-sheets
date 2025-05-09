venv:
	python3 -m venv venv

install: venv
	. venv/bin/activate && pip install -r requirements.txt

run-dev:
	FLASK_ENV=development FLASK_APP=app.py . venv/bin/activate && flask run

db-reset:
	. venv/bin/activate
	alembic downgrade base
	alembic upgrade head

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

docker-clean:
	docker stop whatssheet && docker rm whatssheet

docker-run:
	docker run -d --env-file .env -p $(shell grep -E '^PORT=' .env | cut -d '=' -f2):$(shell grep -E '^PORT=' .env | cut -d '=' -f2) --name whatssheet whatssheet:latest

ngrok-start:
	ngrok http $(shell grep -E '^PORT=' .env | cut -d '=' -f2) > /dev/null 2>&1 & echo $$! > ngrok.pid && sleep 2 && echo "ngrok started with PID $$(cat ngrok.pid)" && curl -s http://127.0.0.1:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -n 1 | sed 's/"public_url":"//;s/"//'

ngrok-stop:
	kill $$(cat ngrok.pid) && rm ngrok.pid && echo "ngrok stopped"

