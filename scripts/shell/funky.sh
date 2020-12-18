#!/bin/bash

##############################################################################
#  funky Shell Integration Script
#
# ----- WHAT DOES THIS SCRIPT DO?
# * Source local and global funks on startup.
# * Source local funks everytime the directory changes.
# * Define two wrapper functions, `funky` and `gfunky`.
#
# ----- INSTALLATION
# In order to take advantage of the full benefits of funky, this script must
# be sourced directly into your .zshrc file. See the official docs for more
# information:
#
#     https://github.com/bbugyi200/funky#additional-installation-steps
##############################################################################

# TODO(bbugyi): Add tests for new behavior.
# TODO(bbugyi): Make funky development environment easier to setup.
# TODO(bbugyi): Allow funky to be installed via -e.
# TODO(bbugyi): Add Dockerfile to funky.

# The FUNKY_CMD envvar must be overridable (e.g. by test_funky.sh).
FUNKY_CMD="${FUNKY_CMD:="$(command -v funky)"}"

##### CREATE FUNKY DATA DIRECTORY
if [ "$EUID" -eq 0 ]; then
    _home_dir=/root
else
    _home_dir="$HOME"
fi

if [[ -n "$XDG_DATA_HOME" ]]; then
    _xdg_data_dir="$XDG_DATA_HOME"/funky
else
    _xdg_data_dir="$_home_dir"/.local/share/funky
fi

[[ -d "$_xdg_data_dir" ]] || mkdir -p "$_xdg_data_dir"

##### HELPER FUNCTIONS
# Source all global funks.
_source_globals() { source <(${FUNKY_CMD} --verbose --global); }

# Source local (per-directory) funks.
_source_locals() { source <(${FUNKY_CMD} --verbose); }

# Get the current TTY number.
_tty_number() { tty | sed 's/[^0-9]*//'; }

# Save PWD and associated funks to disk.
_save_locals() {
    export _ACTIVE_LOCALPATH="$_xdg_data_dir"/localpath-"$(_tty_number)"
    export _ACTIVE_ALIASES="$_xdg_data_dir"/localalias-"$(_tty_number)"

    ${FUNKY_CMD} | sed -E 's/\(.+$//' >"$_ACTIVE_ALIASES"

    if [[ ! -f "$_ACTIVE_LOCALPATH" ]]; then
        echo "$PWD" >"$_ACTIVE_LOCALPATH"
    fi
}

# Unset funks from last directory.
_unset_locals() {
    source <(sed 's/^/unset -f /' "${_ACTIVE_ALIASES}")
    command rm -f "$_ACTIVE_ALIASES"
    unset _ACTIVE_ALIASES
}

# Activate local funks, if necessary.
_maybe_source_locals() {
    if [[ -f "$PWD"/.funky ]]; then
        _source_locals
        if [[ "$PWD" != "$_home_dir" ]]; then
            _save_locals
        fi
    fi
}

# Activate global funks, if necessary.
_maybe_source_globals() {
    if [[ -f "${_home_dir}"/.funky ]]; then
        _source_globals
    fi
}

# Unset old local funks, if necessary.
_maybe_unset_locals() {
    if [[ -f "$_ACTIVE_ALIASES" ]]; then
        _unset_locals
    fi
}

##### SOURCE FUNKS ON STARTUP
_maybe_source_globals
_maybe_source_locals

##### SOURCE APPROPRIATE FUNKS EVERYTIME THE DIRECTORY IS CHANGED
#
# * Is run everytime the directory is changed.
# * Lazily loads global funks and local funks.
chpwd() {
    if [[ -f "$_ACTIVE_LOCALPATH" ]] && ! [[ "$PWD" == $(cat "$_ACTIVE_LOCALPATH") || "$PWD" == "$(cat "$_ACTIVE_LOCALPATH")/"* ]]; then
        _maybe_unset_locals
        _maybe_source_globals
        command rm -f "$_ACTIVE_LOCALPATH"
        unset _ACTIVE_LOCALPATH
    fi

    if [[ "$PWD" != "$_home_dir" ]] && [[ -f "$PWD"/.funky ]]; then
        _maybe_source_locals
        if [[ ! -f "$_ACTIVE_LOCALPATH" ]]; then
            echo "$PWD" >"$_ACTIVE_LOCALPATH"
        fi
    fi
}

PROMPT_COMMAND=chpwd

##### FUNKY'S WRAPPER FUNCTIONS
# Wrapper used to interact with local funks.
unalias funky &>/dev/null
funky() {
    touch "$_xdg_data_dir"/timestamp

    ${FUNKY_CMD} --color=y "$@"
    if [[ .funky -nt "$_xdg_data_dir"/timestamp ]]; then
        _maybe_unset_locals
        _source_locals
    fi
}

# Wrapper used to interact with global funks.
unalias gfunky &>/dev/null
gfunky() {
    touch "$_xdg_data_dir"/timestamp
    ${FUNKY_CMD} --global --color=y "$@"
    if [[ ~/.funky -nt "$_xdg_data_dir"/timestamp ]]; then
        _maybe_unset_locals
        _source_globals
        _maybe_source_locals
    fi
}
