start-docker:
	docker-compose up -d

stop-docker:
	docker-compose rm -sf

run-api-tests:
	nosetests tests/ --with-coverage --cover-package=music_management
	coverage-badge -f -o coverage-api.svg

run-web-tests:
	nosetests tests/ --with-coverage --cover-package=web -s
	coverage-badge -f -o coverage-web.svg

run-tests:
	nosetests tests/ --with-coverage --cover-package=music_management,web -s
	coverage-badge -f -o coverage.svg

install:
	pip install -r music_management/requirements/dev-requirements.txt
	pip install -r web/requirements/dev-requirements.txt