#########################################
#  localalias Shell Integration Script  #
#########################################

##### WHAT DOES THIS SCRIPT DO?
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
# ensure running as root
if [ "$EUID" -eq 0 ]; then
    _home_dir=/root
else
    _home_dir="$HOME"
fi

if [[ -n "$XDG_DATA_HOME" ]]; then
    _xdg_data_dir="$XDG_DATA_HOME"/localalias
else
    _xdg_data_dir="$_home_dir"/.local/share/localalias
fi

[[ -d "$_xdg_data_dir" ]] || mkdir -p "$_xdg_data_dir"

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
    if [[ -f $_xdg_data_dir/localpath ]] && [[ $PWD != "$(cat $_xdg_data_dir/localpath)/"* ]]; then
        _maybe_source_globals
        rm -f $_xdg_data_dir/localpath
    fi

    if [[ $PWD != "$_home_dir" ]] && [[ -f $PWD/.localalias ]]; then
        _source_locals
        if [[ ! -f $_xdg_data_dir/localpath ]]; then
            echo $PWD > $_xdg_data_dir/localpath
        fi
    fi
}

##### Wrapper used to interact with local aliases
unalias la &> /dev/null
la() {
    touch $_xdg_data_dir/timestamp

    localalias --color "$@"
    if [[ .localalias -nt $_xdg_data_dir/timestamp ]]; then
        _source_locals
    fi
}

##### Wrapper used to interact with global aliases
unalias al &> /dev/null
al() {
    touch $_xdg_data_dir/timestamp
    localalias --global --color "$@"
    if [[ ~/.localalias -nt $_xdg_data_dir/timestamp ]]; then
        _source_globals
        _maybe_source_locals
    fi
}
