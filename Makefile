
Pipfile.lock: Pipfile
	pipenv lock && cat Pipfile.lock > $@

.PHONY: test
test: install
	pipenv run pytest -vvvv --cov=registrar --cov-report html tests

.PHONY: clean
clean: clean-build clean-pyc ## clean
	rm -f .installed

.PHONY: clean-build
clean-build:
	rm -fr build/ dist/ *.egg-info .eggs/ .tox/ __pycache__/ .cache/ .coverage htmlcov src

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.installed:
	pipenv install --python 3.6 --dev;
	touch .installed

install: .installed

run-debug-mainnet: .installed
	pipenv run python3.6 -m registrar.cli --dev

run-debug-testnet: .installed
	pipenv run python3.6 -m registrar.cli --dev --testnet
