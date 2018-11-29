include shared.mk


.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: check
check: ## run all tests
	@$(MAKE) --no-print-directory -C tests check

.PHONY: check-python
check-python: ## run python tests
	@$(MAKE) --no-print-directory -C tests check-python

.PHONY: check-python
check-shell: ## run shell tests
	@$(MAKE) --no-print-directory -C tests check-shell

.PHONY: release
release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	ls -l dist

.PHONY: install
install: clean ## install the package to the active Python's site-packages
	python setup.py install
