clean:
	rm -rf build dist *.egg-info
	npm run --prefix mock-site cleanup

setup:
	npm run --prefix mock-site setup

app:
	npm run --prefix mock-site app:detached

tests:
	npm run --prefix mock-site test
	killall phantomjs