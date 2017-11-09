clean:
	rm -rf build dist *.egg-info venv *.pyc .cache
	rm -rf pyseleniumjs/*.pyc pyseleniumjs/tests/*.pyc pyseleniumjs/tests/__pycache__

setup:
# create virtualenv and install test dependencies
	virtualenv venv && venv/bin/pip install -r test-requirements.txt
	npm run --prefix pysjs-mock-site setup

app:
	npm run --prefix pysjs-mock-site app:detached

tests:
# lint package
	venv/bin/pylint pyseleniumjs/e2ejs.py --errors-only
# lint mock site source
	npm run --prefix pysjs-mock-site test
# run e2e tests
	venv/bin/pytest pyseleniumjs/tests

package:
	python setup.py sdist

publish: package
	twine upload dist/*
