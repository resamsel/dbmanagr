executer = dbexec --daemon
COMMAND = executer

ARGS := src/tests/$(COMMAND)/resources
EXPECTED := src/tests/$(COMMAND)/resources/expected
ACTUAL := target/actual-$(COMMAND)

TESTS = $(wildcard $(ARGS)/testcase-*)

target/actual-$(COMMAND)-testcase-%: $(ARGS)/testcase-% $(EXPECTED)/testcase-%
	$($(word 2, $(subst -, , $@))) $(shell scripts/args.sh $(word 1, $^)) > $@
	$(DIFF) $(word 2, $^) $@

test-daemon-$(COMMAND): clean init \
		$(patsubst $(ARGS)/%, $(ACTUAL)-%, $(TESTS))

test-daemon: test-daemon-executer
