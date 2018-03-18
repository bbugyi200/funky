# LocalAlias Bash Script
I use this script to setup aliases and/or functions that are local to a particular directory. Local aliases are stored in a hidden file named `.lshrc` in the current directory. One way to use this script is manually. For example, you could run `LocalAlias` -a' to add an alias and then `LocalAlias -x` to execute that alias, like so:

![Create Alias](img/trial.png "Create Alias")

# Integration with ZSH

The above example doesn't seem too useful at first. When integrated into ZSH, however, it becomes pretty powerful. Placing the below function (`command_not_found_handler`) in your `zshrc` file will override the shell's default behavior for handling invalid commands. Instead of displaying an error message when you type in a bad command, the shell will now attempt to evaluate the command using LocalAlias.

``` bash
command_not_found_handler() {
    WORD=$1; shift
    LocalAlias -x $WORD -- "$@"
}
```

# Demonstration

NOTE: I have aliased `LocalAlias` to `la`.

![Demonstration](img/demo.gif "Demonstration")

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
