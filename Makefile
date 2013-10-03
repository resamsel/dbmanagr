BUILD = build
ARCHIVE = dbexplorer_alfred_0.1.tgz
ALFRED_WORKFLOW = /Volumes/Storage/Dropbox/Alfred/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD

assemble: src
	tar -C $^ -czf $(BUILD)/$(ARCHIVE) .

install: assemble
	tar -C $(ALFRED_WORKFLOW) -xzf $(BUILD)/$(ARCHIVE)

init:
	mkdir $(BUILD)
