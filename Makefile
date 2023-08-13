VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

setup: $(VENV)/bin/activate

run: $(VENV)/bin/activate
	$(PYTHON) sample.py

test: $(VENV)/bin/activate
	$(PYTEST) --cov --cov-report=lcov --cov-branch tests

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
