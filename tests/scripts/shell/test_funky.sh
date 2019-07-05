#!/bin/bash

# shellcheck disable=SC2154

OLD_HOME="${HOME}"; export HOME=/tmp/home

source ./scripts/shell/funky.sh 2> /dev/null

oneTimeSetUp() { 
    mkdir -p /tmp/A/B
    echo '{"my_funk": "echo my_funk_def", "my_override_funk": "echo is_local"}' > /tmp/A/.funky
    echo '{"my_global_funk": "echo my_global_funk_def", "my_override_funk": "echo is_global"}' > "${HOME}"/.funky
}

oneTimeTearDown() {
    export HOME="${OLD_HOME}"

    rm -rf /tmp/A
    rm -rf /tmp/home
}

setUp() { :; }
tearDown() { :; }

###################################################################
#  Maybe Source Tests                                             #
###################################################################
test_maybe_source_locals() {
    pushd /tmp/A &> /dev/null || return 1
    _maybe_source_locals
    popd &> /dev/null || return 1

    type my_funk > /dev/null
    assertEquals 0 "$?"
    assertEquals "my_funk_def" "$(my_funk)"
}

test_maybe_source_globals() {
    _maybe_source_globals

    type my_global_funk > /dev/null
    assertEquals 0 "$?"
    assertEquals "my_global_funk_def" "$(my_global_funk)"
}

###################################################################
#  chpwd() Function Tests                                         #
###################################################################
test_chpwd() {
    cd /tmp/A || return 1
    chpwd
    assertEquals "is_local" "$(my_override_funk)"
    assertEquals "/tmp/A" "$(cat /tmp/home/.local/share/funky/localpath)"

    cd /tmp/A/B || return 1
    chpwd
    assertEquals "is_local" "$(my_override_funk)"
    assertEquals "/tmp/A" "$(cat /tmp/home/.local/share/funky/localpath)"

    cd /tmp || return 1
    chpwd
    assertEquals "is_global" "$(my_override_funk)"
    test -f /tmp/home/.local/share/funky/localpath
    assertEquals 1 "$?"
}


source shunit2
