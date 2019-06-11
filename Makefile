develop:
	# Develop via the docker containers
	# See docker-compose.yml where the `scraper` service is defined
	docker-compose run -e SCRAPER_ENV=development -e PYTHONPATH=. scraper bash

lint:
	black . --check
	flake8 .

format:
	isort -rc -m 3 --trailing-comma --line-width 88 .
	black .

test:
	# Run tests via the docker containers.
	# See docker-compose.yml where the `scraper` service is defined
	docker-compose run -e SCRAPER_ENV=test scraper bash -c "pytest -s"
