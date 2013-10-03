BUILD = build
ARCHIVE = dbexplorer_alfred_0.1.zip
ALFRED_WORKFLOW = /Volumes/Storage/Dropbox/Alfred/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD

assemble: src/*
	zip -j $(BUILD)/$(ARCHIVE) $^

install: assemble
	unzip -f $(BUILD)/$(ARCHIVE) -d $(ALFRED_WORKFLOW)

init:
	mkdir $(BUILD)

