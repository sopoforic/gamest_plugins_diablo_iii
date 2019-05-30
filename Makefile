SOURCES=README.md setup.py gamest_plugins/diablo_iii/__init__.py gamest_plugins/diablo_iii/module.py

test: $(SOURCES)
	@python3.7 setup.py test

dist: $(SOURCES) test
	@python3.7 setup.py sdist bdist_wheel

pypi: dist
	@twine upload dist/*

.PHONY: dist pypi test
