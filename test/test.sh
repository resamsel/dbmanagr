#!/bin/bash

ACTUAL_PREFIX="build/test/"
ACTUAL_SUFFIX=""
EXPECTED_PREFIX="test/suite/expected/"
EXPECTED_SUFFIX=""

TT=$(ruby -e 'puts "%.3f" % Time.now')
STATUS=0
TOTAL=$#
OK=0
FAILED=0

while (( "$#" )); do
	TESTCASE="$(basename ${1%})"
	ACTUAL="$ACTUAL_PREFIX$TESTCASE$ACTUAL_SUFFIX"
	EXPECTED="$EXPECTED_PREFIX$TESTCASE$EXPECTED_SUFFIX"
	SCRIPT="python -m pkg.dbnavigator -s $(cat test/suite/$TESTCASE)"

	echo -n "Testing $TESTCASE... "
	T=$(ruby -e 'puts "%.3f" % Time.now')
	PYTHONPATH=build/files $SCRIPT > $ACTUAL
	T=$(ruby -e 'puts "%.3f" % (Time.now - '$T')')

	DIFF=$(diff -u $EXPECTED $ACTUAL)

	if [ "$DIFF" != "" ]; then
		FAILED=$((FAILED+1))
		echo "FAILED (took ${T}s)"
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
		echo "OK (took ${T}s)"
	fi

	shift
done

TT=$(ruby -e 'puts "%.3f" % (Time.now - '$TT')')

#echo "Tests run: $TOTAL, failed: $FAILED (took ${TT}s)"
#echo

exit $STATUS
