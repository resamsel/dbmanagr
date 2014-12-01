# May be overridden by environment variables
MAKE ?= make
PYTHON ?= python
FLAKE8 ?= flake8
SED ?= gsed
GIT ?= git
ZIP ?= zip
UNZIP ?= unzip
PIP ?= pip
ALFRED_WORKFLOW ?= "$(HOME)/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD"
BASH_COMPLETION_TARGET ?= /usr/local/etc/bash_completion.d

VERSION = src/dbnav/version.py
TARGET = target
SETUPTOOLS = $(PYTHON) setup.py
DIST = dist
PIP_DEPS = flake8 pep8-naming flake8-todo
ACTUAL = $(TARGET)/testfiles/actual
RESOURCES = resources/alfred/*
BASH_COMPLETION_SOURCE = resources/bash_completion/dbnav
ARCHIVE = $(DIST)/Database\ Navigator.alfredworkflow
ALFRED = $(TARGET)/alfred

init:
	mkdir -p $(TARGET) $(TARGET)/test $(ACTUAL) $(TARGET)/files

assemble: init assemble-main assemble-alfred

assemble-main:
	$(SETUPTOOLS) bdist_egg

assemble-alfred: assemble-main $(RESOURCES)
	rm -rf $(ALFRED)
	mkdir -p $(ALFRED)
	cp -r $(RESOURCES) $(ALFRED)
	cp dist/dbnav*-py2.7.egg $(ALFRED)
	sh $(ALFRED)/info.plist.sh
	rm $(ALFRED)/info.plist.sh
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

test: init
	$(FLAKE8) src
	$(SETUPTOOLS) test

develop:
	$(SETUPTOOLS) develop

README.md: develop resources/README.md.sh
	sh $(word 2, $^)
	$(PYTHON) scripts/toc.py $@

release-%:
	$(SED) 's/__version__ = "[^"]*"/__version__ = "$(@:release-%=%)"/g' -i $(VERSION)
	$(MAKE) README.md
	$(GIT) rm dist/dbnav*-py2.7.egg
	$(SETUPTOOLS) bdist_egg
	$(GIT) add dist/dbnav-$(@:release-%=%)-py2.7.egg

clean:
	$(SETUPTOOLS) clean --all
	rm -rf $(TARGET)
	rm -rf $(DIST)
	rm -f .dbnavigator.cache*
