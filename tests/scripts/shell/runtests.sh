#!/bin/bash

# shellcheck disable=SC2154

source ./scripts/shell/funky.sh 2> /dev/null

oneTimeSetUp() { :; }
oneTimeTearDown() { :; }
setUp() { :; }
tearDown() { :; }

source shunit2
