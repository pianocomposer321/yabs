import pynvim
import json
from subprocess import Popen


@pynvim.plugin
class BuildSystem:
    def __init__(self, vim):
        self.vim = vim

    @pynvim.command("NewProject", sync=True)
    def new_project(self):
        # Currently only does the same thing as make-python-project script at /usr/local/bin/make-python-project

        try:
            Popen(["git", "init"])
            with open(".gitignore") as file:
                text = """
                .*
                __pycache__
                !/.gitignore
                """
                file.write(text)
        except FileNotFoundError:
            print("Warning: Git not installed")

    @pynvim.command("EditProjectFile", sync=True)
    def edit_project_file(self):
        pass
