#!/bin/bash

if ! command -v shunit2 &>/dev/null && ! [[ -f ./shunit2 ]]; then
    printf 1>&2 "[ERROR] shunit2 is not installed: https://github.com/kward/shunit2\n"
    exit 1
fi

OLD_HOME="${HOME}"; export HOME=/tmp/home
export FUNKY_CMD="python3 -m funky"

eval "$(${FUNKY_CMD} --init bash)"

oneTimeSetUp() {
    mkdir -p "${HOME}"
    mkdir -p /tmp/A/B
    echo '{"my_funk": "echo my_funk_def", "my_override_funk": "echo is_local"}' > /tmp/A/.funky
    echo '{"my_global_funk": "echo my_global_funk_def", "my_override_funk": "echo is_global"}' > "${HOME}"/.funky
}

oneTimeTearDown() {
    export HOME="${OLD_HOME}"
    unset FUNKY_CMD

    rm -rf /tmp/A
    rm -rf /tmp/home
}

setUp() { :; }
tearDown() { :; }

function assert_funk_defined() { _assert_funk "$@" 0; }
function assert_funk_not_defined() { _assert_funk "$@" 1; }
function _assert_funk() {
    local funk_name="$1"
    shift

    local error_msg="$1"
    shift

    local lineno="$1"
    shift

    local ec="$1"
    shift

    type "${funk_name}" &>/dev/null
    assertEquals "[LINE #${lineno} | ${error_msg}]" "${ec}" "$?"
}

###################################################################
#  Maybe Source Tests                                             #
###################################################################
test_maybe_source_locals() {
    pushd /tmp/A &> /dev/null || return 1
    _maybe_source_locals
    popd &> /dev/null || return 1

    assert_funk_defined "my_funk" "/tmp/A's my_funk() funk is NOT defined in the test_maybe_source_locals test." "${LINENO}"
    assertEquals "my_funk_def" "$(my_funk)"
}

test_maybe_source_globals() {
    _maybe_source_globals

    assert_funk_defined "my_global_funk" "The global my_global_funk() funk is NOT defined in the test_maybe_source_globals test." "${LINENO}"
    assertEquals "my_global_funk_def" "$(my_global_funk)"
}

###################################################################
#  chpwd() Function Tests                                         #
###################################################################
test_chpwd() {
    local tty_number="$(tty | sed 's/[^0-9]*//')"
    local localpath="localpath-${tty_number}"

    cd /tmp/A || return 1
    chpwd
    assertEquals "is_local" "$(my_override_funk)"
    assertEquals "/tmp/A" "$(cat /tmp/home/.local/share/funky/"${localpath}")"

    assert_funk_defined "my_funk" "/tmp/A's my_funk() funk is NOT defined when in /tmp/A!" "${LINENO}"

    cd /tmp || return 1
    chpwd
    assertEquals "is_global" "$(my_override_funk)"
    test -f /tmp/home/.local/share/funky/"${localpath}"
    assertEquals 1 "$?"

    assert_funk_not_defined "my_funk" "/tmp/A's my_funk() funk is still defined when in /tmp!" "${LINENO}"
}


source shunit2
