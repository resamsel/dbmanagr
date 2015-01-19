# May be overridden by environment variables
MAKE ?= make
PYTHON ?= python
FLAKE8 ?= flake8
INSTRUMENTAL ?= instrumental
SED ?= gsed
GIT ?= git
ZIP ?= zip
UNZIP ?= unzip
PIP ?= pip
FIND ?= find
DIFF ?= diff
ALFRED_WORKFLOW ?= "$(HOME)/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD"
BASH_COMPLETION_TARGET ?= /usr/local/etc/bash_completion.d

VERSION = src/dbnav/version.py
TARGET = $(PWD)/target
SETUPTOOLS = $(PYTHON) setup.py
TEST_NOSE = nosetests --with-coverage --cover-package=dbnav --cover-html \
	--cover-html-dir=$(TARGET)/coverage
TEST_INSTRUMENTAL = $(INSTRUMENTAL) -S -t dbnav setup.py $(TEST_NOSE)
TEST = $(SETUPTOOLS) $(TEST_NOSE)
INSTRUMENTAL_REPORT = $(INSTRUMENTAL) -r --xml
DIST = dist
PIP_DEPS = flake8 pep8-naming flake8-todo
ALFRED_RESOURCES = resources/alfred
RESOURCES = $(ALFRED_RESOURCES)/*
BASH_COMPLETION_SOURCE = resources/bash_completion/dbnav
ARCHIVE = $(DIST)/Database\ Navigator.alfredworkflow
ALFRED = $(TARGET)/alfred

init:
	mkdir -p $(TARGET)

assemble: init assemble-main assemble-alfred

assemble-main:
	$(SETUPTOOLS) bdist_egg

assemble-alfred: assemble-main $(RESOURCES)
	rm -rf $(ALFRED)
	mkdir -p $(ALFRED)
	cp -r $(RESOURCES) $(ALFRED)
	cp dist/dbnav*-py2.7.egg $(ALFRED)
	rm -f $(ARCHIVE)
	cd $(ALFRED); $(ZIP) -rq ../../$(ARCHIVE) . \
		--exclude images/.DS_Store "images/dbnavigator.sketch/*"

build: assemble test

install-alfred: assemble-alfred
	$(UNZIP) -oq $(ARCHIVE) -d $(ALFRED_WORKFLOW)

install-bash-completion:
	mkdir -p $(BASH_COMPLETION_TARGET)
	cp $(BASH_COMPLETION_SOURCE) $(BASH_COMPLETION_TARGET)

install: assemble install-bash-completion
	$(SETUPTOOLS) install

missing-copyright:
	$(FIND) . -name "*.py" -exec grep -L 'Copyright' {} \;

test: init
	$(FLAKE8) src
	$(TEST)

clean-daemon:
	rm -rf $(TARGET)/actual-*

test-daemon: clean-daemon

include $(wildcard includes/*.mk)

instrumental: init
	$(FLAKE8) src
	$(TEST_INSTRUMENTAL)
	$(INSTRUMENTAL_REPORT)

develop:
	$(SETUPTOOLS) develop

README.md: develop resources/README.md.sh
	sh $(word 2, $^)
	$(PYTHON) scripts/toc.py $@

debug:
	echo $(PWD)

release-%:
	$(SED) 's/__version__ = "[^"]*"/__version__ = "$(@:release-%=%)"/g' \
		-i $(VERSION) $(ALFRED_RESOURCES)/alfred.py
	$(MAKE) README.md
	$(GIT) rm dist/dbnav*-py2.7.egg
	$(SETUPTOOLS) bdist_egg
	$(GIT) add dist/dbnav-$(@:release-%=%)-py2.7.egg
	$(MAKE) assemble-alfred

clean:
	$(SETUPTOOLS) clean --all
	$(FIND) . -name "*.pyc" -delete
	rm -rf $(TARGET)
	rm -rf $(DIST)
	rm -f .dbnavigator.cache*
	rm -f .coverage .instrumental.cov
