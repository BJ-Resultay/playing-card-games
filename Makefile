# Date:	25 Aug 2023
# Revision History:
#	resultay | 25-08-23 | Add documentation
#
##    ___  __          _____            __
##   / _ \/ /__ ___ __/ ___/__ ________/ /
##  / ___/ / _ `/ // / /__/ _ `/ __/ _  / 
## /_/  /_/\_,_/\_, /\___/\_,_/_/  \_,_/  
## ------------/___/--------------------------------
## help:     Show this
## setup:    Set up virtual environment
## run:      Run sample
## test:     Run tests
##           TEST=/directory/or/file/for/tests
## coverage: Run tests coverage
##           SOURCE=/directory/for/coverage
##           TEST=/directory/or/file/for/tests
## lint:     Lint all python files
## clean:    Remove pycaches and virtual environment
## -------------------------------------------------

PYTHONPATH = :./sample:./src
SOURCE = src
TEST = tests
VENV = venv
PIP = $(VENV)/bin/pip
COVERAGE = $(VENV)/bin/coverage
PYLINT = $(VENV)/bin/pylint
PYTEST = $(VENV)/bin/pytest
PYTHON = $(VENV)/bin/python3

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

setup: $(VENV)/bin/activate

run: $(VENV)/bin/activate
	env PYTHONPATH=$(PYTHONPATH) $(PYTHON) sample/main.py

test: $(VENV)/bin/activate
	env PYTHONPATH=$(PYTHONPATH) $(PYTEST) -rP $(TEST)

coverage: $(VENV)/bin/activate
	$(COVERAGE) run --source=$(SOURCE) -m pytest $(TEST)
	coverage report

lint: $(VENV)/bin/activate
	find . -type f -not -path "./$(VENV)/*" -name "*.py" | xargs $(PYLINT)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
