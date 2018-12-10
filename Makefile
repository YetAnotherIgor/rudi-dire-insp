##
# Makefile for dev chores for this project.
#
# Caveats:
# * Assumes you are on a Linux/MacOS like operating system.  Is NOT compatible with Windows.
# * Assumes you already have Python etc. setup
#
##

SHELL := /bin/bash
export TOXENV = $(shell python3 -c "import sys; print(\"py{}{}\".format(sys.version_info.major, sys.version_info.minor))")

.PHONY: all build check clean docs dist check_tests test

all: clean check check_tests test build docs dist

clean:
	@echo "********************************************************************************"
	@echo	
	@echo "Clean"
	@echo	
	@echo "********************************************************************************"

	-rm -rv build/ dist/ .eggs/ *.egg-info/
	-find . -name "*.pyc" -delete
	-find . -name "*.pyo" -delete
	-find . -name "__pycache__" -delete
	-find . -name '*.egg' -delete

clean_all: clean
	@echo "********************************************************************************"
	@echo	
	@echo "Clean all"
	@echo	
	@echo "********************************************************************************"

	-rm -r .tox/ .pytest/ .mypy_cache/
	-rm -f .coverage
	-rm pytest.log
	mkdir .pytest

.tox/$(TOXENV)/bin/pylint:
	tox --notest

check: .tox/$(TOXENV)/bin/pylint
	@echo "********************************************************************************"
	@echo	
	@echo "Run static checks on source code"
	@echo	
	@echo "********************************************************************************"

	# First pylint
	.tox/$(TOXENV)/bin/pylint rudi_dire_insp

	# Now mypy
	.tox/$(TOXENV)/bin/mypy rudi_dire_insp

check_tests: .tox/$(TOXENV)/bin/pylint
	@echo "********************************************************************************"
	@echo	
	@echo "Run static checks on test code"
	@echo	
	@echo "********************************************************************************"

	# First pylint
	.tox/$(TOXENV)/bin/pylint --errors-only tests

	# Now mypy
	.tox/$(TOXENV)/bin/mypy --ignore-missing-imports tests

test:
	@echo "********************************************************************************"
	@echo	
	@echo "Run tests"
	@echo	
	@echo "********************************************************************************"

	@echo	
	@echo "Running the unit and integration tests via pytest"	
	@echo	

	tox -- test

	@echo	
	@echo "Running the project's command line in a virtualenv as a smoke test of the setup.py config"
	@echo	

	tox -- develop
	.tox/$(TOXENV)/bin/rudi-dire-insp --help


build:
	@echo "********************************************************************************"
	@echo	
	@echo "Build"
	@echo	
	@echo "********************************************************************************"

	tox -- build

docs:
	@echo "********************************************************************************"
	@echo	
	@echo "Build Sphinx Docs"
	@echo	
	@echo "********************************************************************************"
	tox -- sphinx_build 


dist: clean
	@echo "********************************************************************************"
	@echo	
	@echo "Prepare a distribution of the project"
	@echo	
	@echo "********************************************************************************"

	tox -- sdist
	tox -- bdist_wheel
	ls -l dist/

