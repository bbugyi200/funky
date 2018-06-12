#########################################
#  localalias Shell Integration Script  #
#########################################

##### WHAT DOES THIS SCRIPT DO?
# TODO

##### INSTALLATION
# In order to take advantage of the full benefits of localalias, this script must either be used as
# an oh-my-zsh plugin or be sourced directly into your .bashrc / .zshrc file. See the official docs
# for more information:
# 
# https://localalias.readthedocs.io/en/latest/installation.html#additional-installation-steps

## Disable aliases and unwanted builtins
for i in {a..z}; do
    unalias "$i" &> /dev/null
done

arr=("la" "ls" "ll")
for i in "${arr[@]}"; do
    unalias "$i" &> /dev/null
done

disable r

## Source aliases on startup
if [[ -f ~/.globalalias ]]; then
    localalias --global | source /dev/stdin
fi

if [[ -f $PWD/.localalias ]]; then
    localalias | source /dev/stdin
fi

## Source local aliases everytime the directory is changed
chpwd() {
    if [[ -f $PWD/.localalias ]]; then
        localalias | source /dev/stdin
    fi 
}

## Used to interact with local aliases
la() {
    touch /tmp/localalias.timestamp
    localalias --color "$@"
    if [[ .localalias -nt /tmp/localalias.timestamp ]]; then
        localalias | source /dev/stdin
    fi
}

## Used to interact with global aliases
al() {
    touch /tmp/localalias.timestamp
    localalias --global --color "$@"
    if [[ ~/.globalalias -nt /tmp/localalias.timestamp ]]; then
        localalias --global | source /dev/stdin
    fi
}
