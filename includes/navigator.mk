navigator = DBEXPLORER_CFG= NAVICAT_CFG= PGPASS_CFG= \
	SQLITEPASS_CFG=resources/sqlitepass dbnav -T --daemon
COMMAND = navigator

ARGS := src/tests/$(COMMAND)/resources
EXPECTED := src/tests/$(COMMAND)/resources/expected
ACTUAL := target/actual-$(COMMAND)

TESTS = $(wildcard $(ARGS)/testcase-*)

init-daemon-$(COMMAND):
	dbdaemon stop

target/actual-$(COMMAND)-testcase-%: $(ARGS)/testcase-% $(EXPECTED)/testcase-%
	$($(word 2, $(subst -, , $@))) $(shell scripts/args.sh $(word 1, $^)) > $@
	$(DIFF) $(word 2, $^) $@

test-daemon-$(COMMAND): init-daemon-$(COMMAND) \
		$(patsubst $(ARGS)/%, $(ACTUAL)-%, $(TESTS))

test-daemon: test-daemon-navigator
