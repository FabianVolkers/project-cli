#!/usr/bin/env python3
import project as base
from project import frameworks, functions

def create_project(project_class, args):
    print(f"Initialising new {project_class.label} project")
    project = project_class(args.projectname)
    project.initialise()
    return project

def create_environment(project, framework):

    project.initialise_environment()

    if not framework == None:
        project.initialise_framework()

    return project


def create_base_project(args):
    print(f'creating project')
    project = create_project(base.Project, args)
    
    
def create_javascript_project(args):
    print('creating javascript project')


def create_python_project(args):

    framework = args.framework
    framework = "python" if framework == None else framework

    supported_frameworks = functions.get_supported_frameworks(frameworks)

    if f"python.{framework}" in supported_frameworks:
        project = create_project(supported_frameworks[f"python.{framework}"]['class'], args)

    else:
        print(f"framework {framework} not found.")
    
    framework = None if framework == 'python' else framework

    project = create_environment(project, framework)
    project.initialise_structure()



def git_function(args):
    print('git commands')

def readme_function(args):
    print('readme command')

def requirements_function(args):
    print('requirements command')
