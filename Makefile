# May be overridden by environment variables
MAKE ?= make
PYTHON ?= python
SED ?= gsed
GIT ?= git
ZIP ?= zip
UNZIP ?= unzip
PIP ?= pip
FIND ?= find
DIFF ?= diff
RADON ?= radon
ALFRED_WORKFLOW ?= "$(HOME)/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD"
BASH_COMPLETION_TARGET ?= /usr/local/etc/bash_completion.d

# Code quality and coverage
FLAKE8 ?= flake8 --max-complexity=16
PYLINT ?= pylint
INSTRUMENTAL ?= instrumental

VERSION = src/dbnav/version.py
TARGET = target
TARGETS = $(TARGET) $(TARGET)/coverage
SETUPTOOLS = $(PYTHON) setup.py
TEST_NOSE = nosetests --with-coverage --cover-package=dbnav --cover-html \
	--cover-html-dir=$(PWD)/$(TARGET)/coverage
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

$(TARGET)/ijson-2.0.tar.gz = https://pypi.python.org/packages/source/i/ijson/ijson-2.0.tar.gz
$(TARGET)/SQLAlchemy-0.9.8.tar.gz = https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-0.9.8.tar.gz
$(TARGET)/pg8000-1.10.1.tar.gz = https://pypi.python.org/packages/source/p/pg8000/pg8000-1.10.1.tar.gz
$(TARGET)/PyMySQL3-0.5.tar.gz = https://pypi.python.org/packages/source/P/PyMySQL3/PyMySQL3-0.5.tar.gz

init:
	mkdir -p $(TARGETS)

assemble: init assemble-main assemble-alfred

assemble-main:
	$(SETUPTOOLS) bdist_egg

assemble-alfred: assemble-main assemble-ijson assemble-sqlalchemy assemble-postgresql assemble-mysql $(RESOURCES)
	rm -rf $(ALFRED)
	mkdir -p $(ALFRED) $(ALFRED)/lib
	cp -r $(RESOURCES) $(ALFRED)
	cp dist/dbnav*-py2.7.egg $(ALFRED)/lib
	cp $(TARGET)/ijson-2.0/dist/*py2.7*.egg $(ALFRED)/lib
	cp $(TARGET)/SQLAlchemy-0.9.8/dist/*py2.7*.egg $(ALFRED)/lib
	cp $(TARGET)/pg8000-1.10.1/dist/*py2.7*.egg $(ALFRED)/lib
	cp $(TARGET)/PyMySQL3-0.5/dist/*py2.7*.egg $(ALFRED)/lib
	rm -f $(ARCHIVE)
	cd $(ALFRED); $(ZIP) -rq ../../$(ARCHIVE) . \
		--exclude images/.DS_Store "images/dbnavigator.sketch/*"

$(TARGET)/%.tar.gz: init
	curl -o "$@" "$($@)"

$(TARGET)/%: $(TARGET)/%.tar.gz
	tar -C $(TARGET) -xzf "$^"

bdist-%: $(TARGET)/%
	cd $^; $(SETUPTOOLS) bdist_egg

assemble-ijson: bdist-ijson-2.0

assemble-sqlalchemy: bdist-SQLAlchemy-0.9.8

assemble-postgresql: bdist-pg8000-1.10.1

assemble-mysql: bdist-PyMySQL3-0.5

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

check-code:
	$(FLAKE8) src
	$(PYLINT) src/dbnav

metrics:
	$(RADON) cc src --total-average -s -n C
	$(RADON) mi src -s -n B

test: init clean-coverage check-code
	$(TEST)

init-daemon:
	rm -f $(TARGET)/actual-*
	mkdir -p $(TARGET)

test-daemon: init-daemon
	@echo Ran $(shell ls -1 $(TARGET)/actual-* | wc -l) tests: OK

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
	#$(GIT) rm dist/dbnav*-py2.7.egg
	#$(SETUPTOOLS) bdist_egg
	#$(GIT) add dist/dbnav-$(@:release-%=%)-py2.7.egg
	$(MAKE) assemble-alfred

clean-coverage:
	rm -f .coverage .instrumental.cov

clean: clean-coverage
	$(SETUPTOOLS) clean --all
	$(FIND) . -name "*.pyc" -delete
	rm -rf $(TARGET)
	rm -rf $(DIST)
	rm -f .dbnavigator.cache*
