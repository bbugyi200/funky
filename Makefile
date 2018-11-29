include shared.mk


.PHONY: clean
clean: clean-build clean-pyc clean-test ## Remove all build, test, coverage and Python artifacts.

.PHONY: clean-build
clean-build: ## Remove build artifacts.
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## Remove test and coverage artifacts.
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

check check-python check-shell:
	@$(MAKE) --no-print-directory -C tests $@

.PHONY: release
release: dist ## Package and upload a release.
	twine upload dist/*

dist: clean ## Builds source and wheel package.
	python setup.py sdist
	ls -l dist

.PHONY: install
install: clean ## Install the package to the active Python's site-packages.
	python setup.py install
