#!/usr/bin/env bash

if [ "$#" -ne 2 ]; then
	>&2 echo "Usage: $0 <target> <dependency>"
	exit 1
fi

TMP=$(mktemp)
RESULT=$(
	bazel query \
		--noimplicit_deps \
		"filter(\"$2\", deps(\"$1\"))" \
		2>"$TMP"
)
ERR=$(cat "$TMP")
rm "$TMP"

if [ $? -ne 0 ] || [[ "$ERR" == *"ERROR:"* ]]; then
	>&2 echo "Bazel query failed:"
	>&2 echo ""
	>&2 echo "$ERR"
	exit 1
fi

# The pipe to xargs is there to strip any potential whitespace
if [[ $(echo "$RESULT" | xargs) == "$2" ]]; then
	exit 0
else
	exit 1
fi