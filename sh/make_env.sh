#!/usr/bin/env bash

set -x
set -e

if bazel query :requirements.update >/dev/null 2>/dev/null; then
	echo "Updating requirements lock file..."
	bazel run \
		--ui_event_filters=-info,-stdout,-stderr \
		--noshow_progress \
		:requirements.update
fi

bazel run :env env

ROOT=$(bazel info workspace)

if hash direnv 2>/dev/null; then
	CWD=$(pwd)

	if [ -f ".envrc" ]; then
		direnv deny 2>/dev/null || true
	fi

	cat >.envrc <<EOF
export VIRTUAL_ENV="$CWD/env"
export PATH="$CWD/env/bin:$PATH"
EOF

	direnv allow

	if "$ROOT/sh/test_dependency.sh" ":env" "@@rules_python~~pip~pip_312_jupyterlab//:pkg"; then
		PATH="$CWD/env/bin:$PATH" $ROOT/sh/build_jupyter.sh
	fi
fi