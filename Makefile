TARGET = target
DIST = $(TARGET)/dist
ACTUAL = $(TARGET)/testfiles/actual
SUITE = src/test/resources
SOURCES = src/main src/images src/info.plist src/5AD6B622-051E-41D9-A608-70919939967A.png
TEST_SOURCES = src/test/test.sh src/test/main
TEST_RESOURCES = src/test/resources
ARCHIVE = $(TARGET)/Database_Navigator-0.1.alfredworkflow
ALFRED_WORKFLOW ?= "$(HOME)/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD"
TESTCASES = $(shell echo $(SUITE)/testcase-*)
ACTUALS = $(TESTCASES:$(SUITE)/testcase-%=$(ACTUAL)/testcase-%)

init:
	mkdir -p $(TARGET) $(TARGET)/test $(ACTUAL) $(TARGET)/files

clean:
	rm -rf $(TARGET)
	rm -f .dbnavigator.cache

assemble: init main-assemble test-assemble

main-assemble: $(SOURCES)
	rm -rf $(TARGET)/files
	mkdir -p $(TARGET)/files
	cp -r $^ $(TARGET)/files

archive: assemble
	rm -f $(ARCHIVE)
	cd $(TARGET)/files; zip -rq ../../$(ARCHIVE) . \
		--exclude images/.DS_Store "images/dbnavigator.sketch/*" "*.pyc"
#	tar -C $(TARGET)/files -czf $(ARCHIVE) \
#		--exclude=.DS_Store \
#		--exclude="*.sketch" \
#		--exclude="*.pyc" \
#		.

build: archive test

install: build
	unzip -oq $(ARCHIVE) -d $(ALFRED_WORKFLOW)
#	tar -C $(ALFRED_WORKFLOW) -xzf $(ARCHIVE)

test-assemble:
	cp -r $(TARGET)/files/* $(TARGET)/testfiles/
	cp -r $(TEST_SOURCES) $(TARGET)/testfiles/
	cp -r $(TEST_RESOURCES) $(TARGET)/testfiles/

test: assemble $(ACTUALS)

$(ACTUAL)/testcase-%: $(SUITE)/testcase-%
	$(TARGET)/testfiles/test.sh $^
