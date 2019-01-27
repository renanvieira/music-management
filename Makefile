start-docker:
	docker-compose up -d

stop-docker:
	docker-compose rm -sf

run-tests:
	nosetests tests/integration --with-coverage  --cover-package=music_management -s
	coverage-badge -o coverage.svg

install:
	pip install -r requirements/dev-requirements.txt