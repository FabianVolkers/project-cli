from project import Project
import os, sys, subprocess

class PythonProject(Project):
    def __init__(self, name, version=3):
        super().__init__(name)
        self.language = 'python'
        self.version = version

    def initialise_environment(self):
        os.system("python3 -m venv venv")
        os.system("source venv/bin/activate")
    
    def create_requirements(self):
        self.requirements = os.popen("pip freeze")
        with open('requirements.txt', "w") as requirements_file:
            requirements_file.write(self.requirements)




class FlaskProject(PythonProject):
    def __init__(self, name, language, version=3):
        super().__init__(name, version)
        self.framework = 'flask'

    def initialise_framework(self):
        os.system("pip install flask")