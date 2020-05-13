#!/usr/bin/env python3
#TODO: figure out a way to have a generic create project function with all logic caught in classes
from project import frameworks, functions, models

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
    project = create_project(models.Project, args)
    
    
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

def load_project(args):
    try:
        projectfile = args.projectfile
    except AttributeError:
        projectfile = ".project"

    with open(projectfile) as file:
            attributes = file.readlines()
            file.close()
    project_class_str = attributes[0].split("=")[1].split("'")[1].split(".")[2]
    print(project_class_str)
    if hasattr(frameworks.python, project_class_str):
        project_class = getattr(frameworks.python, project_class_str)
    elif hasattr(frameworks.javascript, project_class_str):
        project_class = getattr(frameworks.javascript, project_class_str)
    elif hasattr(models, project_class_str):
        project_class = getattr(models, project_class_str)
    else:
        print("Project class not found")
    name = attributes[1].split("=")[1]
    project = project_class(name)
    project.load(attributes)
    print(project.__dict__)

def git_function(args):
    print('git commands')

def readme_function(args):
    print('readme command')

def requirements_function(args):
    print('requirements command')
