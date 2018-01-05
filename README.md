# LocalAlias Bash Script
I use this script to setup aliases and/or functions that are local to a particular directory. Local aliases are stored in a hidden file named `.lshrc` in the current directory. One way to use this script is manually. For example, you could run `LocalAlias` -a' to add an alias like so:

![Create Alias](img/trial.png "Create Alias")

# Integration with ZSH

The above example doesn't seem to useful at first glance. When integrated into ZSH, however, it becomes pretty powerful. Placing the below function (`command_not_found_handler`) in your `zshrc` file will override the shell's default behavior for handling invalid commands. Instead of displaying an error message when you type in a bad command, the shell will now evaluate the command using LocalAlias.

``` bash
command_not_found_handler() {
    WORD=$1; shift
    LocalAlias -x $WORD -- "$@"
}
```

# Demonstration

NOTE: I have aliased `LocalAlias` to `la`.

![Demonstration](img/demo.gif "Demonstration")
