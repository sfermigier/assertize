.PHONY: all develop test lint clean doc format


# The package name
PKG=assertize


all: test lint

#
# Setup
#
develop: install-deps activate-pre-commit configure-git

install-deps:
	@echo "--> Installing dependencies"
	pip install -U pip setuptools wheel
	poetry install

activate-pre-commit:
	@echo "--> Activating pre-commit hook"
	pre-commit install

configure-git:
	@echo "--> Configuring git"
	git config branch.autosetuprebase always


#
# testing & checking
#
test-all: test test-readme

test:
	@echo "--> Running Python tests"
	pytest --ff -x -p no:randomly
	@echo ""

test-randomly:
	@echo "--> Running Python tests in random order"
	pytest
	@echo ""

test-with-coverage:
	@echo "--> Running Python tests"
	pytest --cov $(PKG)
	@echo ""

test-with-typeguard:
	@echo "--> Running Python tests with typeguard"
	pytest --typeguard-packages=${PKG}
	@echo ""

vagrant-tests:
	vagrant up
	vagrant ssh -c /vagrant/deploy/vagrant_test.sh


#
# Various Checkers
#
lint: lint-py

lint-ci: lint

lint-all: lint lint-mypy

lint-py:
	@echo "--> Linting Python files /w flake8"
	flake8 src tests
	# mypy src tests
	@echo ""

#
# Formatting
#
format: format-py

format-py:
	black src tests
	isort src tests


#
# Everything else
#
install:
	poetry install

clean:
	rm -f **/*.pyc
	find . -type d -empty -delete
	rm -rf *.egg-info *.egg .coverage .eggs .cache .mypy_cache .pyre \
		.pytest_cache .pytest .DS_Store  docs/_build docs/cache docs/tmp \
		dist build pip-wheel-metadata junit-*.xml htmlcov coverage.xml

tidy: clean
	rm -rf .tox

update-deps:
	pip install -U pip setuptools wheel
	poetry update

publish: clean
	git push --tags
	poetry build
	twine upload dist/*
