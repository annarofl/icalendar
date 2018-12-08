.PHONY: docs
init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	# This runs all of the tests, on both Python 2 and Python 3.
	detox

#ci: test coverage
ci: test

test:
	pytest src/ical --junitxml=test_reports/icalendar.xml

test-readme:
	@pipenv run python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst and HISTORY.rst ok") || echo "Invalid markup in README.rst or HISTORY.rst!"

flake8:
	pipenv run flake8 src --ignore=E501,F401,E128,E402,E731,F821 requests

coverage:
#--cov-config .coveragerc 
	pytest --verbose --cov-report term --cov-report xml --cov=icalendar src/ical

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"