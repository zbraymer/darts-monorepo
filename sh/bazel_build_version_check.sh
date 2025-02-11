#!/usr/bin/env bash

BAZEL_VERSION=$(bazel version | awk '/Build label/ {print $3}')
if [[ "$BAZEL_VERSION" != "7.4.1" ]]; then
    echo "Expected Bazel version 7.4.1, but found $BAZEL_VERSION"
    exit 1
fi
