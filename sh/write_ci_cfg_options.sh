#!/usr/bin/env bash

set -e -u -o pipefail

BAZELRC=$(bazel info workspace)/.bazelrc
CI_LINE="import %workspace%/.aspect/bazelrc/ci.bazelrc"

if [[ "$(head -n 1 "$BAZELRC")" != "$CI_LINE" ]]; then
	sed -i "1i\\$CI_LINE" "$BAZELRC"
fi
