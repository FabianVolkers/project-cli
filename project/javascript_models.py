#!/usr/bin/env python3
import project.models as models
import os, sys, subprocess

class JavaScriptProject(models.Project):
    def __init__(self, name, language, framework):
        super().__init__(name, language, framework)


class NodeJSProject(JavaScriptProject):
    def __init__(self, name, language, framework):
        super().__init__(name, language, framework)
    
    def initialise_environment(self):
        self.package_json = f"""
{{
    "name": "{self.name}",
    "version": "{self.version}"

}}
        """
        os.system(f"echo {self.package_json} > package.json")
        os.system('npm init')
    


class VueJSProject(NodeJSProject):
    def __init__(self, name, language, framework):
        super().__init__(name, language, framework)
    
