init:
	pip install -r requirements.txt

test: lint unit-tests

unit-tests:
	nosetests

lint:
	pylint craftai tests

update-readme:
	./scripts/update_readme.sh

version-increment-major:
	./scripts/update_version major

version-increment-minor:
	./scripts/update_version minor

version-increment-patch:
	./scripts/update_version patch
