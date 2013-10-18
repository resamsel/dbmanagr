#!/bin/bash

ACTUAL_PREFIX="build/test/"
ACTUAL_SUFFIX=".actual"
EXPECTED_PREFIX="test/resources/"
EXPECTED_SUFFIX=".expected"
STATUS=0
TOTAL=$#
OK=0
FAILED=0

while (( "$#" )); do
	TESTCASE="$(basename ${1%.sh})"
	ACTUAL="$ACTUAL_PREFIX$TESTCASE$ACTUAL_SUFFIX"
	EXPECTED="$EXPECTED_PREFIX$TESTCASE$EXPECTED_SUFFIX"
	SCRIPT="build/files/$(cat test/resources/$TESTCASE.sh)"

	echo -n "Testing $TESTCASE... "
	$SCRIPT > $ACTUAL

	DIFF=$(diff -u $EXPECTED $ACTUAL)

	if [ "$DIFF" != "" ]; then
		FAILED=$((FAILED+1))
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
		OK=$((OK+1))
		echo OK
	fi

	shift
done

echo "Tests run: $TOTAL, failed: $FAILED"
echo

exit $STATUS
