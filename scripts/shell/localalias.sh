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

setopt ALIAS_FUNC_DEF

if [[ -f ~/.globalalias ]]; then
    localalias --global | source /dev/stdin
fi

if [[ -f $PWD/.localalias ]]; then
    localalias | source /dev/stdin
fi

chpwd() {
    if [[ -f $PWD/.localalias ]]; then
        localalias | source /dev/stdin
    fi 
}

la() {
    touch /tmp/localalias.timestamp
    localalias --color "$@"
    if [[ .localalias -nt /tmp/localalias.timestamp ]]; then
        localalias | source /dev/stdin
    fi
}

al() {
    touch /tmp/localalias.timestamp
    localalias --global --color "$@"
    if [[ ~/.globalalias -nt /tmp/localalias.timestamp ]]; then
        localalias --global | source /dev/stdin
    fi
}
