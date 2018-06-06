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

    localalias -x "$alias" -- "$@"
    exit_status=$?

    if [[ $exit_status -eq 127 ]]; then
        if [[ $OLD_COMMAND_HANDLER = true ]]; then
            orig_command_not_found_handler "$alias"
            return $?
        else
            echo "$error_fmt"
            printf "$error_fmt" "$alias"
            return $exit_status
        fi
    fi
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
