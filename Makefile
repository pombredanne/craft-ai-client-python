init: 
	pip install -r requirements.txt

test: lint unit-tests

unit-tests: 
	nosetests

lint:
	pylint craftai tests
