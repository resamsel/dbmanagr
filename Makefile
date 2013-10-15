BUILD = build
ARCHIVE = dbexplorer_alfred_0.1.tgz
ALFRED_WORKFLOW = /Volumes/Storage/Dropbox/Alfred/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD

$(BUILD)/%:
	mkdir -p $@

init: $(BUILD)/ $(BUILD)/test $(BUILD)/files

assemble: src/*.py src/images
	rm -rf $(BUILD)/files
	mkdir -p $(BUILD)/files
	cp -r $^ $(BUILD)/files

archive: assemble
	rm -f $(BUILD)/$(ARCHIVE)
	tar -C $(BUILD)/files -czf $(BUILD)/$(ARCHIVE) --exclude=.DS_Store --exclude="*.sketch" .

build: init archive test

install: build
	tar -C $(ALFRED_WORKFLOW) -xzf $(BUILD)/$(ARCHIVE)

test: test/resources/testcase*.sh
	test/test.sh $^
