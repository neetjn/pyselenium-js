clean:
	echo "Running cleanup..."
	npm run --prefix test cleanup

setup:
	echo "Setting up..."
	npm run --prefix test setup

app:
	echo "Standing up app"
	npm run --prefix test app:detached

tests:
	echo "Running tests..."
	npm run --prefix test test
