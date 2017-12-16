clean:
	rm -rf build dist *.egg-info venv *.pyc .cache
	rm -rf pyseleniumjs/*.pyc tests/*.pyc tests/__pycache__

setup:
# create virtualenv and install test dependencies
	virtualenv venv && venv/bin/pip install -r tests/test-requirements.txt
	npm run --prefix tests/pysjs-mock-site setup

app:
	npm run --prefix tests/pysjs-mock-site app:detached

test:
# lint package
	venv/bin/pylint pyseleniumjs/e2ejs.py --errors-only
# run e2e tests
	venv/bin/pytest --cov=pyseleniumjs tests/*.py

package:
	python setup.py sdist

publish: package
	twine upload dist/*
