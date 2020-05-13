#!/usr/bin/env python3
""" import project.models as models
import project.functions as functions
import project.template as template """
from project import models, functions, template
import os, sys, subprocess

class PythonProject(models.Project):
    def __init__(self, name, version=3):
        super().__init__(name)
        self.language = 'python'
        self.version = version
        self.framework = "python"


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

    def initialise_structure(self):
        filenames = {
            "module": ["__init__.py", f"{self.name}.py"],
            "docs": ["conf.py"],
            "tests": ["context.py", "test_basic.py", "test_advanced.py"]
        }
        for section in filenames:
            if section == "module":
                path = f"{self.path}/{self.name}"
            else:
                path = f"{self.path}/{section}"

            setattr(self, section, path)

            os.mkdir(path)
            files = filenames[section]
            for filename in files:
                functions.create_file_from_template(
                    f"{path}/{filename}", self, filename
                    )


    def create_requirements(self):
        
        pip_freeze_command = f"{self.pip} freeze"
        stdout, stderr, returncode = functions.run_process(pip_freeze_command)
        if returncode == 0:
            print(pip_freeze_command)
            self.requirements = stdout
            functions.create_file(f"{self.path}/requirements.txt", self.requirements)


    def install_packages(self, packages):
        install_cmd = f"{self.pip} install {' '.join(packages)}"
        print(f"Installing python packages {', '.join(packages)} and dependencies using {self.pip}")
        stdout, stderr, returncode = functions.run_process(install_cmd)
        if returncode == 0:
            lines = stdout.split("\n")
            print(lines[len(lines)-2])
            return True
        else:
            print(stderr)
            return False





class FlaskProject(PythonProject):
    def __init__(self, name, version=3):
        super().__init__(name, version)
        self.framework = 'flask'


    def initialise_framework(self):
        packages = ['flask', 'python-dotenv']
        if self.install_packages(packages):
            return True

        else:
            print(f"Error installing packages {', '.join(packages)} and dependecies using pip.")
            print(f"Try installing them manually using this command:\n")
            print(f"{self.pip} install {' '.join(packages)}")
    



    def initialise_structure(self):
        self.app = "app"
        self.routes = "routes"
        self.app_dir = f"{self.path}/{self.app}"
        stdout, stderr, returncode = functions.run_process(f"mkdir {self.app_dir}")
        if returncode == 0:

            self.create_app()
            self.create_routes()
            self.create_main()

            # Save FLASK_APP in .flaskenv
            functions.create_file(f"{self.path}/.flaskenv", f"FLASK_APP={self.name}.py")


            print("\tSuccessfully generated flask project.\n")
            print(f"\tStored environment variable FLASK_APP={self.name}.py in {self.path}/.flaskenv\n")
            print("\tTo activate the virtual environment run:\n")
            print(f"\tcd {self.path} && source {self.env}/bin/activate\n")
            print("\tTo start the development server, run:\n")
            print("\tflask run\n")


    
    def create_app(self):
        path = f"{self.app_dir}/__init__.py"
        content = f"""
from flask import Flask

app = Flask(__name__)

from {self.app} import {self.routes}
"""
        functions.create_file(path, content)

    
    def create_routes(self):
        path = f"{self.app_dir}/{self.routes}.py"
        content = f"""
from {self.app} import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
"""
        functions.create_file(path, content)


    def create_main(self):
        path = f"{self.path}/{self.name}.py"
        content = f"""
from {self.app} import app
"""
        functions.create_file(path, content)




class DjangoProject(PythonProject):
    def __init__(self, name, version=3):
        super().__init__(name, version=version)