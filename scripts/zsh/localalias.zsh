# unalias 'la' which is bound as an entry point for localalias
if [[ $(type -w la) == 'la: alias' ]]; then
    unalias la
fi

# reroutes command not found errors to localalias
command_not_found_handler() {
    CMD=$1; shift

    localalias -x "$CMD" -- "$@"
    exit_status=$?

    if [[ $exit_status -eq 127 ]]; then
        echo "zsh: command not found: $CMD"
    fi

    return $exit_status
}
