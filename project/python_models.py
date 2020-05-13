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

    def initialise_structure(self):
        self.initialise_module()
        self.initialise_docs()
        self.initialise_tests()
        

    def initialise_module(self):
        self.module = f"{self.path}/{self.name}"
        os.mkdir(self.module)
        open(f"{self.module}/__init__.py", "w").close()
        open(f"{self.module}/{self.name}.py", "w").close()

    def initialise_docs(self):
        self.docs = f"{self.path}/docs"
        os.mkdir(self.docs)
        open(f"{self.docs}/conf.py", "w").close()


    def initialise_tests(self):
        self.tests = f"{self.path}/tests"
        os.mkdir(self.tests)

        context = f"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from ...{self.name} import {self.name}
"""
        functions.create_file(f"{self.tests}/context.py", context)

        tests = f"from .context import {self.name}"
        functions.create_file(f"{self.tests}/test_basic.py", tests)
        functions.create_file(f"{self.tests}/test_advanced.py", tests)

    def create_requirements(self):
        
        pip_freeze_command = f"{self.pip} freeze"
        stdout, stderr, returncode = functions.run_process(pip_freeze_command)
        if returncode == 0:
            print(pip_freeze_command)
            self.requirements = stdout
        with open('requirements.txt', "w") as requirements_file:
            requirements_file.write(self.requirements)

    def install_packages(self, packages):
        install_cmd = f"{self.pip} install {packages.join(' ')}"
        print(f"Installing python packages {packages.join(', ')} and dependencies using {self.pip}")
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
            self.initialise_app()

        else:
            print(f"Error installing packages {packages.join(', ')} and dependecies using pip.")
            print(f"Try installing them manually using this command:\n")
            print(f"{self.pip} install {packages.join(' ')}")
    



    def initialise_app(self):
        self.app = "app"
        self.routes = "routes"
        self.app_dir = f"{self.path}/{self.app}"
        stdout, stderr, returncode = functions.run_process(f"mkdir {self.app_dir}")
        if returncode == 0:

            self.create_app()
            self.create_routes()
            self.create_main()

            # Save FLASK_APP in .flaskenv
            with open(f"{self.path}/.flaskenv", "x") as file:
                file.write(f"FLASK_APP={self.name}.py")
                file.close()

            print("Successfully generated flask project.\n")
            print(f"Stored environment variable FLASK_APP={self.name}.py in {self.path}/.flaskenv\n")
            print("To activate the virtual environment run:\n")
            print(f"cd {self.path} && source {self.env}/bin/activate\n")
            print("To start the development server, run:\n")
            print("flask run\n")


    
    def create_app(self):
        path = f"{self.app_dir}/__init__.py"
        try:
            with open(path, 'x') as file:
                content = f"""
from flask import Flask

app = Flask(__name__)

from {self.app} import {self.routes}
"""
                file.write(content)
                file.close()
            print(f"created {path}")
        except FileExistsError:
            print(f"{path} already exists, not overwriting.")
    
    def create_routes(self):
        path = f"{self.app_dir}/{self.routes}.py"
        try:
            with open(path, "x") as file:
                content = f"""
from {self.app} import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
"""
                file.write(content)
                file.close()
            print(f"created {path}")        
        except FileExistsError:
            print(f"{path} already exists, not overwriting.")

    def create_main(self):
        path = f"{self.path}/{self.name}.py"
        try:
            with open(path, "x") as file:
                content = f"""
from {self.app} import app
"""
                file.write(content)
                file.close()
            print(f"created {path}")
        except FileExistsError:
            print(f"{path} already exists, not overwriting.")



class DjangoProject(PythonProject):
    def __init__(self, name, version=3):
        super().__init__(name, version=version)