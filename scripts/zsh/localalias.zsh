# reroutes command not found errors to localalias
command_not_found_handler() {
    CMD=$1; shift
    if ! localalias -x $CMD -- "$@"; then
        echo "zsh: command not found: $CMD"
        return 127
    fi
}
