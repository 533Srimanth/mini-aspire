run: clean create-venv
	. my_env/bin/activate; python3 -m pip install -r requirements.txt; flask --app src/main.py run

install-venv:
	sudo apt install python3-venv

test: clean create-venv
	. my_env/bin/activate; python3 -m pip install -r requirements.txt; python3 -m pip install pytest pytest-cov; pytest --cov --cov-report=html:coverage

create-venv: install-venv
	python3 -m venv my_env

clean:
	rm -rf my_env
