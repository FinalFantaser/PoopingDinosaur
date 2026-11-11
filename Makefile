ifeq ($(OS),Windows_NT)
    PYTHON ?= py -3.12
    VENV_PYTHON := venv/Scripts/python.exe
else
    PYTHON ?= python3
    VENV_PYTHON := venv/bin/python
endif

venv:
	$(PYTHON) -m .venv venv

install: venv
	$(VENV_PYTHON) -m pip install -r requirements.txt

run: install
	$(VENV_PYTHON) main.py