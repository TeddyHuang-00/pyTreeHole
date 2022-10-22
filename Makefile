PY?=python3
BUILD?=python3 -m build

BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/build

TEST_PUBLISH_SITE=testpypi
PUBLISH_SITE=pypi

clean:
	- rm -rf $(OUTPUTDIR)

build:
	$(BUILD) --outdir $(OUTPUTDIR)

rebuild: clean build

test-publish: rebuild
	$(PY) -m twine upload --repository $(TEST_PUBLISH_SITE) $(OUTPUTDIR)/*

publish: rebuild
	$(PY) -m twine upload --repository $(PUBLISH_SITE) $(OUTPUTDIR)/*

.PHONY: clean build rebuild test-publish publish