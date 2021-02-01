import pynvim
import json
import re
# import subprocess as sp
import os
import shutil


@pynvim.plugin
class BuildSystem:
    def __init__(self, vim):
        self.vim = vim
        self.cwd = self.vim.eval("getcwd()")

        # self.project_types = ["Python", "Rust", "C++"]
        self.project_types = self.get_project_types()
        self.project_type = None
        self.add_new_string = "Add new type..."

        self._default_vars = {
            "file": self.get_file,
            "file_base_name": self.get_file_base_name,
            "folder": self.get_folder
        }

        self._sources_dict = {
            "vim": self.vim_source,
            "neoterm": self.neoterm_source,
            "tmux": self.tmux_source,
            "toggleterm": self.toggleterm_source,
            "floaterm": self.floaterm_source
        }

        self._load_config()

    def _load_config(self, config_path=""):
        if config_path == "":
            config_path = os.path.expanduser("~") + "/.config/yabs"

        full_path = config_path + "/config.json"
        with open(full_path, "r") as file:
            data = json.load(file)

        self.source = self._sources_dict[data['source']]

    def get_project_types(self, path=None):
        if path is None:
            path = os.path.expanduser("~") + "/.config/yabs/build-systems"

        types = {}

        for file_name in os.listdir(path):
            with open(f"{path}/{file_name}", "r") as file:
                data = json.load(file)
                # types.append(data["name"])
                types[data["name"]] = file_name

        return types

    def get_file(self):
        return self.vim.eval("expand('%')")

    def get_file_base_name(self):
        return self.vim.eval("expand('%:r')")

    def get_folder(self):
        return self.vim.eval("expand('%:h')")

    @pynvim.command("NewBuildSystem", sync=True)
    def new_build_system(self):
        self.project_type = self.vim.eval(f'Finder({str(list(self.project_types) + [self.add_new_string])}, "Select Project Type")[0]')
        if self.project_type == self.add_new_string:
            pass  # TODO: read project_types from file instead of from hard-coded variable
        else:
            # shutil.copyfile(f'{os.path.expanduser("~")}/.config/yabs/build-systems/{self.project_types[self.project_type]}.json')
            home = os.path.expanduser("~")
            filename = self.project_types[self.project_type]
            shutil.copyfile(f"{home}/.config/yabs/build-systems/{filename}", f'{self.cwd}/{filename}')

    @pynvim.command("EditProjectFile", sync=True)
    def edit_project_file(self):
        self.vim.command(f'edit {self.cwd}/project.json')

    @pynvim.command("Build")
    def build(self):
        self.vim.command("wall")
        if os.path.isfile(f'{self.cwd}/.project.json'):
            self.build_project()
        else:
            self.build_file()

    @pynvim.command("BuildProject")
    def build_project(self):
        if os.path.isfile(".project.json"):
            path = ".project.json"
        else:
            filetype = self.vim.eval("&filetype")
            path = f"{os.path.expanduser('~')}/.config/yabs/build-systems/{filetype}.json"

        data = self.load_json_file(path)
        command = self.parse_json(data)
        self.source(command)

    @pynvim.command("BuildFile")
    def build_file(self):
        command = self.parse_json()
        self.source(command)

    def parse_json(self, data=None):
        if data is None:
            data = self.load_json_file()

        vars = data["vars"] if "vars" in data else {}
        build_cmd = data["build_cmd"]
        args = build_cmd.split()

        hashtag = re.compile(r"#{(.*?)}")
        dollar = re.compile(r"\${(.*?)}")

        for arg in args:
            hmatches = hashtag.findall(arg)
            dmatches = dollar.findall(arg)

            for match in hmatches:
                if match in vars:
                    build_cmd = re.sub(r"#{" + match + r"}", vars[match], build_cmd)
                else:
                    self.vim.command("echo 'feature not yet implemented'")

            for match in dmatches:
                if match in self._default_vars:
                    build_cmd = re.sub(r"\${" + match + r"}", self._default_vars[match](), build_cmd)
                else:
                    self.vim.command('echo "Error in filetype\'s json file"')

        return build_cmd

    def load_json_file(self, path=None):
        if path is None:
            # return self.load_json_file(f"{os.path.expanduser("~")}")
            filetype = self.vim.eval("&filetype")
            path = f"{os.path.expanduser('~')}/.config/yabs/default-commands/{filetype}.json"

        with open(path, "r") as file:
            data = json.load(file)
        return data

    def vim_source(self, command):
        self.vim.command("!" + command)

    def tmux_source(self, command):
        self.vim.command("call SendTmuxCommand('{command}')")

    def neoterm_source(self, command, term_height=12):
        self.vim.command(f"call NeotermRunCommand('{command}')")

    def toggleterm_source(self, command):
        self.vim.command(f"TermExec {command}")

    def floaterm_source(self, command):
        # self.vim.command(f"call FloatermRunCommand('{command}')")
        buffers = self.vim.eval('getbufinfo()')
        terminal = re.compile(r'^term:\/\/')
        runner_open = False

        for buf in buffers:
            if terminal.match(buf['name']) and 'floaterm_name' in buf['variables']:
                if buf['variables']['floaterm_name'] == 'yabs-runner':
                    runner_open = True
                    break

        if runner_open:
            self.vim.command(f"FloatermSend --name=yabs-runner {command}")
            self.vim.command("FloatermShow yabs-runner")
        else:
            self.vim.command(f"FloatermNew! --cwd={self.cwd} --name=yabs-runner --height=12 --width=0.97 --position=bottom --autoclose=1 {command}")
