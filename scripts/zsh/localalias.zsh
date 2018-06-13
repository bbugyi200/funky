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

##### Disable aliases
for i in {a..z}; do
    unalias "$i" &> /dev/null
done

for i in {0..9}; do
    unalias "$i" &> /dev/null
done

arr=("la" "ls" "ll")
for i in "${arr[@]}"; do
    unalias "$i" &> /dev/null
done

##### Disable builtins
disable r

##### Create temporary localalias directory
_temp_path=/tmp/localalias

if [[ ! -d $_temp_path ]]; then
    mkdir $_temp_path
fi

##### Function used for sourcing aliases
_source_globals() { localalias --global | source /dev/stdin; }
_source_locals() { localalias | source /dev/stdin; }

_maybe_source_locals() {
    if [[ -f $PWD/.localalias ]]; then
        _source_locals
    fi
}

_maybe_source_globals() {
    if [[ -f ~/.globalalias ]]; then
        _source_globals
    fi
}

##### Source aliases on startup
_maybe_source_globals
_maybe_source_locals

##### Source local aliases everytime the directory is changed
chpwd() {
    if [[ -f $_temp_path/localpath ]] && [[ $PWD != "$(cat $_temp_path/localpath)"* ]]; then
        _maybe_source_globals
        rm -f $_temp_path/localpath
    fi

    if [[ -f $PWD/.localalias ]]; then
        _source_locals
        if [[ ! -f $_temp_path/localpath ]]; then
            echo $PWD > $_temp_path/localpath
        fi
    fi
}

##### Wrapper used to interact with local aliases
la() {
    touch $_temp_path/timestamp
    localalias --color "$@"
    if [[ .localalias -nt $_temp_path/timestamp ]]; then
        _source_locals
    fi
}

##### Wrapper used to interact with global aliases
al() {
    touch $_temp_path/timestamp
    localalias --global --color "$@"
    if [[ ~/.globalalias -nt $_temp_path/timestamp ]]; then
        _source_globals
        _maybe_source_locals
    fi
}
