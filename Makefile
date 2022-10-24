PY?=python3
BUILD?=python3 -m build
DOC?=pdoc
TEST?=pytest

DOC_BRANCH?=gh-pages
DOC_PORT?=8000
DOC_OPTS+=-c latex_math=True

NAME=treehole

BASE_DIR=$(CURDIR)
OUTPUT_DIR=$(BASE_DIR)/build
DOC_DIR=$(BASE_DIR)/docs
SRC_DIR=$(BASE_DIR)/src/$(NAME)

TEST_PUBLISH_SITE=testpypi
PUBLISH_SITE=pypi

build:
	$(BUILD) --outdir $(OUTPUT_DIR)

rebuild: clean build

test-publish: rebuild
	$(PY) -m twine upload --repository $(TEST_PUBLISH_SITE) $(OUTPUT_DIR)/*

publish: rebuild
	$(PY) -m twine upload --repository $(PUBLISH_SITE) $(OUTPUT_DIR)/*

run-tests:
	$(TEST) $(BASE_DIR)

docs: docs-clean
	$(DOC) --html --output-dir $(DOC_DIR) $(DOC_OPTS) $(SRC_DIR)

docs-dev:
	$(DOC) --http localhost:8000 $(DOC_OPTS) $(SRC_DIR)

docs-publish: docs
	- git branch -D $(DOC_BRANCH)
	ghp-import -n -o -m "Generate docs $(shell date -u +"%Y-%m-%d %H:%M:%S")" -b $(DOC_BRANCH) $(DOC_DIR)/$(NAME)
	git push -f origin $(DOC_BRANCH)

clean:
	- rm -rf $(OUTPUT_DIR)

docs-clean:
	- rm -rf $(DOC_DIR)

.PHONY: build rebuild test-publish publish run-tests docs docs-dev docs-publish clean docs-clean