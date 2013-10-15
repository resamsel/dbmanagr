#!/bin/bash

while (( "$#" )); do
	TESTCASE=$(basename ${1%.sh})
	ACTUAL=/tmp/test-$RANDOM.actual
	EXPECTED=test/resources/$TESTCASE.expected

	echo -n "Testing $TESTCASE... "
	sh test/resources/$TESTCASE.sh > $ACTUAL

	DIFF=$(diff -u $ACTUAL $EXPECTED)

	if [ "$DIFF" != "" ]; then
		echo FAILED
		echo $DIFF
	else
		echo OK
	fi

	shift
done
