clean:
	rm -rf build dist *.egg-info
	npm run --prefix test cleanup

setup:
	npm run --prefix test setup

app:
	npm run --prefix test app:detached

tests:
	npm run --prefix test test
	killall phantomjs