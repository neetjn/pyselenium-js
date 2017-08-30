clean:
	rm -rf build dist *.egg-info venv *.pyc .cache ghostdriver.log
	rm -rf pyseleniumjs/*.pyc pyseleniumjs/tests/*.pyc pyseleniumjs/tests/__pycache__
	npm run --prefix mock-site cleanup

setup:
# create virtualenv and install test dependencies
	virtualenv venv && venv/bin/pip install -r test-requirements.txt
	npm run --prefix mock-site setup

app:
	npm run --prefix mock-site app:detached

tests:
# lint package
	venv/bin/pylint pyseleniumjs/e2ejs.py --errors-only
# lint mock site source
	npm run --prefix mock-site lint
# run e2e tests
	venv/bin/pytest pyseleniumjs/tests
# kill dangling phantomjs instances
	killall phantomjs

package:
	python setup.py sdist