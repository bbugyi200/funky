#########################################
#  localalias Shell Integration Script  #
#########################################

##### WHAT DOES THIS SCRIPT DO?
# - Disables single letter aliases and builtins (these are desirable for use as local aliases)
# - Source local and global aliases on startup.
# - Source local aliases everytime the directory changes.
# - Define two wrapper functions, `la` and `al`.

##### INSTALLATION
# In order to take advantage of the full benefits of localalias, this script must either be used as
# an oh-my-zsh plugin or be sourced directly into your .bashrc / .zshrc file. See the official docs
# for more information:
# 
# https://localalias.readthedocs.io/en/latest/installation.html#additional-installation-steps

##### Create temporary localalias directory
_temp_path=/tmp/localalias

if [[ ! -d $_temp_path ]]; then
    mkdir $_temp_path
fi

##### Function used for sourcing aliases
_source_globals() { localalias --verbose --global | source /dev/stdin; }
_source_locals() { localalias --verbose | source /dev/stdin; }

_maybe_source_locals() {
    if [[ -f $PWD/.localalias ]]; then
        _source_locals
    fi
}

_maybe_source_globals() {
    if [[ -f ~/.localalias ]]; then
        _source_globals
    fi
}

##### Source aliases on startup
_maybe_source_globals
_maybe_source_locals

##### Source appropriate aliases everytime the directory is changed
#
# - Is run everytime the directory is changed.
# - Lazily loads global aliases and local aliases while attempting to maintain parent's local
#   aliases.
chpwd() {
    if [[ -f $_temp_path/localpath ]] && [[ $PWD != "$(cat $_temp_path/localpath)/"* ]]; then
        _maybe_source_globals
        rm -f $_temp_path/localpath
    fi

    if [[ $PWD != /home/$USER ]] && [[ -f $PWD/.localalias ]]; then
        _source_locals
        if [[ ! -f $_temp_path/localpath ]]; then
            echo $PWD > $_temp_path/localpath
        fi
    fi
}

##### Wrapper used to interact with local aliases
unalias la &> /dev/null
la() {
    touch $_temp_path/timestamp

    localalias --color "$@"
    if [[ .localalias -nt $_temp_path/timestamp ]]; then
        _source_locals
    fi
}

##### Wrapper used to interact with global aliases
unalias al &> /dev/null
al() {
    touch $_temp_path/timestamp
    localalias --global --color "$@"
    if [[ ~/.localalias -nt $_temp_path/timestamp ]]; then
        _source_globals
        _maybe_source_locals
    fi
}
