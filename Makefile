ifeq ($(OS),Windows_NT)
    PYTHON := venv\Scripts\python.exe
    PIP := venv\Scripts\pip.exe
    RM := rmdir /s /q
else
    PYTHON := venv/bin/python
    PIP := venv/bin/pip
    RM := rm -rf
endif

.PHONY: venv install run clean

venv:
	python -m venv venv

install: venv
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) main.py

clean:
	$(RM) venv