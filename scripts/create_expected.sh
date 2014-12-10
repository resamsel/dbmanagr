#!/bin/bash

TEST="$1"
EXPECTED="$(dirname "$TEST")/expected/$(basename "$TEST")"

shift

#echo $EXPECTED
(echo "dbnav $*"; cat "$TEST") | tr '\n' ' ' | sh > "$EXPECTED"
