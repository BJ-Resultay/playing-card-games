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
##           OPTIONS='any other options'
##           TEST=/directory/or/file/for/tests
## coverage: Run tests coverage
##           SOURCE=/directory/for/coverage
##           OPTIONS='any other options'
##           TEST=/directory/or/file/for/tests
## lint:     Lint all python files
## clean:    Remove pycaches and virtual environment
## -------------------------------------------------

OPTIONS =
SOURCE = src
TEST = tests
VENV = venv
BIN = $(VENV)/bin
PIP = $(BIN)/pip
COVERAGE = $(BIN)/coverage
PYLINT = $(BIN)/pylint
PYTEST = $(BIN)/pytest
PYTHON = $(BIN)/python3

.PHONY: setup run test coverage lint clean help

$(BIN)/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

setup: $(BIN)/activate

run: setup
	$(PYTHON) sample/main.py

test: setup
ifdef OPTIONS
	$(PYTEST) $(OPTIONS) $(TEST)
else
	$(PYTEST) $(TEST)
endif

coverage: setup
ifdef OPTIONS
	$(COVERAGE) run --source=$(SOURCE) $(OPTIONS) -m pytest $(TEST)
else
	$(COVERAGE) run --source=$(SOURCE) -m pytest $(TEST)
endif
	coverage report

lint: setup
	find . -type f -not -path "./$(VENV)/*" -name "*.py" | xargs $(PYLINT)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
