BUILD = build
ACTUAL = $(BUILD)/test/actual
SUITE = test/suite
SOURCES = src/pkg src/images src/info.plist src/5AD6B622-051E-41D9-A608-70919939967A.png
ARCHIVE = $(BUILD)/dbexplorer_alfred_0.1.tgz
ALFRED_WORKFLOW = /Volumes/Storage/Dropbox/Alfred/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD
TESTS = $(shell echo $(SUITE)/testcase-*)
ACTUALS = $(TESTS:$(SUITE)/testcase-%=$(ACTUAL)/testcase-%)

init:
	mkdir -p $(BUILD) $(BUILD)/test $(ACTUAL) $(BUILD)/files

clean:
	rm -rf $(BUILD)
	rm -f .dbnavigator.cache

assemble: init _assemble

_assemble: $(SOURCES)
	rm -rf $(BUILD)/files
	mkdir -p $(BUILD)/files
	cp -r $^ $(BUILD)/files

archive: assemble
	rm -f $(ARCHIVE)
	tar -C $(BUILD)/files -czf $(ARCHIVE) --exclude=.DS_Store --exclude="*.sketch" .

build: archive test

install: build
	tar -C $(ALFRED_WORKFLOW) -xzf $(ARCHIVE)

test: assemble $(ACTUALS)

$(ACTUAL)/testcase-%: $(SUITE)/testcase-%
	test/test.sh $^
