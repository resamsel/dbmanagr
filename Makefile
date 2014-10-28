VERSION = src/dbnav/version.py
TARGET = target
SETUPTOOLS = python setup.py
DIST = dist
ACTUAL = $(TARGET)/testfiles/actual
SOURCES = src/images src/info.plist src/5AD6B622-051E-41D9-A608-70919939967A.png
BASH_COMPLETION_SOURCE = src/bash_completion/dbnav
BASH_COMPLETION_TARGET = ~/.bash_completion.d
ARCHIVE = $(DIST)/Database\ Navigator.alfredworkflow
ALFRED = $(TARGET)/alfred
ALFRED_WORKFLOW ?= "$(HOME)/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD"

init:
	mkdir -p $(TARGET) $(TARGET)/test $(ACTUAL) $(TARGET)/files

clean:
	$(SETUPTOOLS) clean
	rm -rf $(TARGET)
	rm -f .dbnavigator.cache

assemble: init assemble-main assemble-alfred

assemble-main:
	$(SETUPTOOLS) bdist_egg

assemble-alfred: $(SOURCES)
	rm -rf $(ALFRED)
	mkdir -p $(ALFRED)
	cp -r $^ $(ALFRED)
	rm -f $(ARCHIVE)
	cd $(ALFRED); zip -rq ../../$(ARCHIVE) . \
		--exclude images/.DS_Store "images/dbnavigator.sketch/*"

archive: assemble

build: archive test

install-alfred: assemble-alfred
	unzip -oq $(ARCHIVE) -d $(ALFRED_WORKFLOW)

install-bash-completion:
	mkdir -p $(BASH_COMPLETION_TARGET)
	cp $(BASH_COMPLETION_SOURCE) $(BASH_COMPLETION_TARGET)

install: assemble install-bash-completion
	$(SETUPTOOLS) install

test:
	$(SETUPTOOLS) test

develop:
	$(SETUPTOOLS) develop

usage-%:
	sh generate-help.sh $(@:usage-%=%)

release-%: usage-dbnav usage-dbgraph usage-dbdiff usage-dbexport usage-dbexec
	gsed 's/dbnav-[^-]*-py2.7.egg/dbnav-$(@:release-%=%)-py2.7.egg/g' -i README.md
	gsed 's/__version__ = "[^"]*"/__version__ = "$(@:release-%=%)"/g' -i $(VERSION)
	git rm dist/dbnav*-py2.7.egg
	$(SETUPTOOLS) bdist_egg
	git add dist/dbnav-$(@:release-%=%)-py2.7.egg
