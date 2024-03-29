#!/bin/bash

#################################################################################
#  funky Shell Integration Script
#
# ----- WHAT DOES THIS SCRIPT DO?
# * Source local and global funks on startup.
# * Source local funks everytime the directory changes.
# * Define two wrapper functions, `funky` and `gfunky`.
#
# ----- INSTALLATION
# In order to take advantage of the full benefits of funky, this script must be
# sourced directly into your .bashrc or .zshrc file. Use `funky --setup-shell
# SHELL` (where SHELL is either 'bash' or 'zsh') to set this up automatically.
#################################################################################

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
_source_locals() { source <(${FUNKY_CMD} --verbose) && _save_locals; }

# Get the current TTY number.
_tty_number() { tty | sed 's/[^0-9]*//'; }

# Save PWD and associated funks to disk.
_save_locals() {
    export _ACTIVE_LOCALPATH="$_xdg_data_dir"/localpath-"$(_tty_number)"
    export _ACTIVE_ALIASES="$_xdg_data_dir"/localalias-"$(_tty_number)"

    ${FUNKY_CMD} | perl -nE 'print s/\(.+$//gr if /^\S+\(/' >"$_ACTIVE_ALIASES"

    if [[ ! -f "$_ACTIVE_LOCALPATH" ]]; then
        echo "$PWD" >"$_ACTIVE_LOCALPATH"
    fi
}

# Unset funks from last directory.
_unset_locals() {
    source <(perl -nE 'print s{^(.*)$}{unset -f \1 &>/dev/null}gr' "${_ACTIVE_ALIASES}")
    command rm -f "$_ACTIVE_ALIASES"
    unset _ACTIVE_ALIASES
}

# Unset old local funks, if necessary.
_maybe_unset_locals() {
    if [[ -f "$_ACTIVE_ALIASES" ]]; then
        _unset_locals
    fi
}

# Activate global funks, if necessary.
_maybe_source_globals() {
    if [[ -f "${_home_dir}"/.funky ]]; then
        _source_globals
    fi
}

# Activate local funks, if necessary.
_maybe_source_locals() {
    if [[ -f "$PWD"/.funky ]] && [[ "$PWD" != "${_home_dir}" ]]; then
        _source_locals
    fi
}

# Setup the proper funk environment.
function _setup_funks() {
    _maybe_unset_locals
    _maybe_source_globals
    _maybe_source_locals
}

##### SOURCE FUNKS ON STARTUP
_setup_funks

##### SOURCE APPROPRIATE FUNKS EVERYTIME THE DIRECTORY IS CHANGED
#
# * Is run everytime the directory is changed.
# * Lazily loads global funks and local funks.
chpwd() {
    if [[ -f "$_ACTIVE_LOCALPATH" ]] && ! [[ "$PWD" == $(cat "$_ACTIVE_LOCALPATH") ]]; then
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
funky() { _funky .funky "$@"; }

# Wrapper used to interact with global funks.
unalias gfunky &>/dev/null
gfunky() { _funky ~/.funky --global "$@"; }

# Helper function used by funky's main wrapper functions.
function _funky() {
    local funk_defs_file="$1"
    shift

    touch "$_xdg_data_dir"/timestamp

    ${FUNKY_CMD} --color=y "$@"
    if [[ "${funk_defs_file}" -nt "$_xdg_data_dir"/timestamp ]]; then
        _setup_funks
    fi
}
