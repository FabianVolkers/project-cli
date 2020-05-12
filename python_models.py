#!/usr/bin/env python3
from project import Project
import functions
import os, sys, subprocess

class PythonProject(Project):
    def __init__(self, name, version=3):
        super().__init__(name)
        self.language = 'python'
        self.version = version


    def initialise_environment(self):
        create_venv_command = f"python3 -m venv {self.path}/venv"
        stdout, stderr, returncode = functions.run_process(create_venv_command)
        if returncode == 0:
            print(create_venv_command)
            self.env = f"{self.path}/venv"
            self.pip = f"{self.env}/bin/pip"
            self.python = f"{self.env}/bin/python"

            return True

        else:
            print(stderr)
    
    def create_requirements(self):
        
        pip_freeze_command = f"{self.pip} freeze"
        stdout, stderr, returncode = functions.run_process(pip_freeze_command)
        if returncode == 0:
            print(pip_freeze_command)
            self.requirements = stdout
        with open('requirements.txt', "w") as requirements_file:
            requirements_file.write(self.requirements)




class FlaskProject(PythonProject):
    def __init__(self, name, version=3):
        super().__init__(name, version)
        self.framework = 'flask'


    def initialise_framework(self):
        install_flask_command = f"{self.pip} install flask"
        stdout, stderr, returncode = functions.run_process(install_flask_command)
        if returncode == 0:
            print(install_flask_command)
            print(stdout)
        else:
            print(stderr)