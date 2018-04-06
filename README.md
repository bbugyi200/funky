# Demonstration

NOTE: I have aliased `LocalAlias` to `la`.

![Demonstration](img/demo.gif "Demonstration")

# LocalAlias Bash Script
I use this script to setup aliases and/or functions that are local to a particular directory. Local aliases are stored in a hidden file named `.lshrc` in the current directory. One way to use this script is manually. For example, you could run `LocalAlias` -a' to add an alias and then `LocalAlias -x` to execute that alias, like so:

![Create Alias](img/trial.png "Create Alias")

A better way to make use of this script is described in the [Integration with ZSH](#integration-with-zsh) section.

# Installation Notes

Installing LocalAlias is as simple as copying the script to a directory that is on your systems `PATH`. An ideal location for unix systems would be `/usr/local/bin`.

### Dependencies

* `gnu-getopt`: Not all versions of `getopt` support long options (i.e. `--help`). You can verify that you're using the new version of getopt by running `getopt -T; echo $?`. If you get back a positive number, you're using the newer version and should be good to go.
* `pygmentize`: Needed if you want to use the `-c / --color` option.

### Integration with ZSH

The above example doesn't seem too useful at first. When integrated into ZSH, however, it becomes pretty powerful. Placing the below function (`command_not_found_handler`) in your `zshrc` file will override the shell's default behavior for handling invalid commands. Instead of displaying an error message when you type in a bad command, the shell will now attempt to evaluate the command using LocalAlias.

``` bash
command_not_found_handler() {
    WORD=$1; shift
    LocalAlias -x $WORD -- "$@"
}
```
# Command-Line Options
Command-line options for `LocalAlias`:
<pre>
-a | --alias                        Add &lt;word> as an alias.
-f &lt;word> | --function &lt;word>       Add &lt;word> as a function.
-r &lt;word> | --remove &lt;word>         Remove the alias/function &lt;word>.
-e [word] | --edit [word]           Edit .lshrc. If [word] is provided, the cursor will start on [word]'s' definition.
-x &lt;word> | --execute &lt;word>        Execute the alias/function defined for &lt;word> if one exists. Otherwise, prompt user to add &lt;word> as an alias/function.
-p [word] | --print [word]          Prints the either the contents of .lshrc or (if [word] is provided) just the definition for [word]. This option is the default.
-v | --verbose                      Enable verbose output.
-c | --color                        Colorize output (requires `pygmentize`)
-d | --debug                        Enable debug mode.
</pre>

# Additional Features

If you preface an alias with `@T ` (e.g. `alias cdd='@T cd /home/john/Downloads'`), the aliased command will be run using `tmux send-keys`. This is useful for aliasing commands that you need to run in the current shell (the `cd` command being a good example). Obviously, you will need to have tmux installed and be running inside a tmux session for this to work.
