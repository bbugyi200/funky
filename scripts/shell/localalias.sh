#########################################
#  localalias Shell Integration Script  #
#########################################

##### WHAT DOES THIS SCRIPT DO?
# This script redefines how your shell reacts when you try to use a shell command that does not
# exist. With this script installed, your shell will check if any local aliases exist with that
# "bad" command name first, instead of immediately raising an error. If no local aliases are found
# that match the given command name, the shell then reacts the same as it would had this script
# never been installed.

##### INSTALLATION
# In order to take advantage of the full benefits of localalias, this script must either be used as
# an oh-my-zsh plugin or be sourced directly into your .bashrc / .zshrc file. See the official docs
# for more information:
# 
# https://localalias.readthedocs.io/en/latest/installation.html#additional-installation-steps

_save_old_command_handler() {
    if declare -f "$1" > /dev/null; then
        eval "$(echo "orig_command_not_found_handler(){"; declare -f "$1" | tail -n +2)"
        OLD_COMMAND_HANDLER=true
    else
        OLD_COMMAND_HANDLER=false
    fi
}

# reroutes command not found errors to localalias
_command_not_found_template() {
    error_fmt="$1"; shift
    alias="$1"; shift

    localalias -x "$alias" "$@"
    exit_status=$?

    if [[ $exit_status -eq 127 ]]; then
        if [[ $OLD_COMMAND_HANDLER = true ]]; then
            orig_command_not_found_handler "$alias"
            return $?
        else
            printf "$error_fmt" "$alias"
        fi
    fi

    return $exit_status
}

case "${SHELL}" in
    */zsh)
        _save_old_command_handler "command_not_found_handler"
        command_not_found_handler() {
            _command_not_found_template "zsh: command not found: %s\n" "$@"
            return $?
        }
        ;;
    */bash)
        _save_old_command_handler "command_not_found_handle"
        command_not_found_handle() {
            _command_not_found_template "bash: %s: command not found\n" "$@"
            return $?
        }
        ;;
esac
