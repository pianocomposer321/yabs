YABS is a sublime-text-like build system for vim. The way it works is that it
creates a .project file in the root of your project. This file tells the plugin
how to build and run your project. There are defaults for several filetypes
included in the ~/.config/yabs folder. For example, the default for python is
the following:

```json
{
    "build_cmd": "python3 ${file}"
}
```

This file tells the plugin to run the current file.

You can also use the "vars" object in the json to define variables to be used in
the rest of the json with the "#{}" notation. #{} variables may reference each
other. For example, if you were using a project where the entry point for the
program is "main.py" instead of the current file, you could have a project.json
file such as the following:

```json
{
    "vars": {
        "entry_point": "main.py"
    },
    "build_cmd": "python3 #{entry_point}"
}
```

The default project files live in ~/.config/yabs/default-commands and are named
for the filetype that they build. So the default python file is called
"python.json", the default C++ file is "cpp.json", etc.

The default keybinding for executing the compile command is "<leader><cr>". This
can be changed by remapping the <plug>(yabs-build) binding.

When starting a new project, you can select a build system from the list of
files in ~/.config/yabs/build-systems. The default build system for python
projects is the following (the same as the example above):

```json
{
    "vars": {},
    "build_cmd": "python3 #{entry_point:main.py}"
}
```

Upon finding this file, the plugin will look in the json file for any variables
referenced with the #{} notation that were not set in the "vars" object. It will
then prompt you for values to fill in for them. In the above example, the plugin
would prompt you for a value for the "entry_point" variable. If a value is
supplied after a colon, as in the above example, that value will be auto-filled
in the input prompt, so all the user needs to do is press enter.


${} vars:
file
file_base_name
file_extension
