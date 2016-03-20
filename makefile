init:
	pip install -r requirements.txt

test:
	py.test -v

coverage:
	coverage run --source=vigilance setup.py test
	coverage report

report:
	coverage
	open htmlcov/index.html
