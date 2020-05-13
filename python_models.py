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
        install_flask_command = f"{self.pip} install flask python-dotenv"
        stdout, stderr, returncode = functions.run_process(install_flask_command)
        if returncode == 0:
            #print(install_flask_command)
            lines = stdout.split("\n")
            print(lines[len(lines)-2])

            self.initialise_app()


        else:
            print(stderr)
    



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
            print("To activate the virtual environment run:\n")
            print(f"cd {self.path} && source {self.env}/bin/activate")
            print("To start the development server, run:\n")
            print("flask run")


    
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