#!/bin/bash

STATUS=0

while (( "$#" )); do
	TESTCASE=$(basename ${1%.sh})
	ACTUAL=/tmp/test-$TESTCASE.actual
	EXPECTED=test/resources/$TESTCASE.expected
	SCRIPT="build/files/$(cat test/resources/$TESTCASE.sh)"

	echo -n "Testing $TESTCASE... "
	$SCRIPT > $ACTUAL

	DIFF=$(diff -u $EXPECTED $ACTUAL)

	if [ "$DIFF" != "" ]; then
		echo FAILED
		echo $SCRIPT
		if [ "$(which colordiff)" != "" ]; then
			echo colordiff $EXPECTED $ACTUAL
			colordiff $EXPECTED $ACTUAL
		else
			echo diff -u $EXPECTED $ACTUAL
			echo $DIFF
		fi
		STATUS=-1
	else
		echo OK
	fi

	shift
done

exit $STATUS
