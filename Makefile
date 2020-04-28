doc:
	rm -Rf html
	pdoc --html mfutil

clean:
	rm -Rf html htmlcov
	rm -Rf mfutil.egg-info
	find . -type d -name __pycache__ -exec rm -Rf {} \; 2>/dev/null || exit 0

test: clean
	pytest tests/

coverage:
	pytest --cov-report html --cov=mfutil tests/
	pytest --cov=mfutil tests/
