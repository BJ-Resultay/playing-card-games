VENV = venv
PIP = $(VENV)/bin/pip
PYLINT = $(VENV)/bin/pylint
PYTEST = $(VENV)/bin/pytest
PYTHON = $(VENV)/bin/python3

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

setup: $(VENV)/bin/activate

lint: $(VENV)/bin/activate
	find . -type f -not -path "./$(VENV)/*" -name "*.py" | xargs $(PYLINT)

run: $(VENV)/bin/activate
	$(PYTHON) sample/main.py

test: $(VENV)/bin/activate
	$(PYTEST) --cov --cov-report=lcov --cov-branch -rP tests

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
