PY?=python3
BUILD?=python3 -m build
DOC?=pdoc
TEST?=pytest
VER_TEST?=vermin

DOC_BRANCH?=gh-pages
DOC_OPTS+=-d markdown --math

TEST_OPTS+=--durations=0 --json-report --json-report-summary --json-report-file=$(TST_DIR)/tmp.json
TEST_POST_SCRIPT?=$(TST_DIR)/process_test_result.py
VER_TEST_OPTS+=--eval-annotations --backport dataclasses --backport typing -vv

NAME=treehole

BASE_DIR=$(CURDIR)
OUTPUT_DIR=$(BASE_DIR)/build
DOC_DIR=$(BASE_DIR)/docs
SRC_DIR=$(BASE_DIR)/src/$(NAME)
TST_DIR=$(BASE_DIR)/tests

TEST_PUBLISH_SITE=testpypi
PUBLISH_SITE=pypi

build:
	$(BUILD) --outdir $(OUTPUT_DIR)

rebuild: clean build

test-publish: rebuild
	$(PY) -m twine upload --repository $(TEST_PUBLISH_SITE) $(OUTPUT_DIR)/*

publish: rebuild
	$(PY) -m twine upload --repository $(PUBLISH_SITE) $(OUTPUT_DIR)/*

unit-tests:
	- $(TEST) $(TEST_OPTS) $(BASE_DIR)
	$(PY) $(TEST_POST_SCRIPT)

version-test:
	$(VER_TEST) $(VER_TEST_OPTS) $(SRC_DIR)

docs: docs-clean
	$(DOC) $(SRC_DIR) $(DOC_OPTS) -o $(DOC_DIR)

docs-publish: docs
	- git branch -D $(DOC_BRANCH)
	ghp-import -n -o -m "Generate docs $(shell date -u +"%Y-%m-%d %H:%M:%S")" -b $(DOC_BRANCH) $(DOC_DIR)
	git push -f origin $(DOC_BRANCH)

clean:
	- rm -rf $(OUTPUT_DIR)

docs-clean:
	- rm -rf $(DOC_DIR)

.PHONY: build rebuild test-publish publish unit-tests docs docs-dev docs-publish clean docs-clean