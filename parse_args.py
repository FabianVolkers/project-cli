#!/usr/bin/env python3
import argparse
import frameworks, functions
import project as base

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



def git_function(args):
    print('git commands')

def readme_function(args):
    print('readme command')

def requirements_function(args):
    print('requirements command')

def add_language_subparser(frameworks, subparser):
    supported_languages = []
    frameworks = dict(sorted(frameworks.items()))
    # helper iterable for accessing next item
    iter_frameworks = iter(frameworks)
    next(iter_frameworks)

    for framework in frameworks:
        _curr = frameworks[framework]

        try:
            _next = frameworks[next(iter_frameworks)]
        except StopIteration:
            _next = {'lang': None}

        if not _curr['lang'] in supported_languages:
            supported_languages.append(_curr['lang'])
            supported_frameworks = []

        supported_frameworks.append(frameworks[framework]['class'].label)
        
        if _curr['lang'] == _next['lang']:
            continue
        else:
            new_subparser = subparser.add_parser(_curr['lang'], help=f"create {_curr['lang']} projects")
            new_subparser.add_argument('-f', '--framework', type=str, choices=supported_frameworks)
            new_subparser.set_defaults(func=_curr['create_func'])

def add_documentation_subparser(subparsers):
    """Maybe refactor readme and requirements into single subparser named documentation"""
    readme_parser = subparsers.add_parser('readme', help='readme related commands')
    readme_parser.add_argument('command', type=str, choices=['create', 'show', 'update'])
    readme_parser.add_argument('-g', '--git', nargs=2, type=str, help='Push updated README to git remote', metavar=('remote', 'branch'))
    readme_parser.set_defaults(func=readme_function)

    requirements_parser = subparsers.add_parser('requirements', help='requirements commands')
    requirements_parser.add_argument('command', type=str, choices=['create', 'show', 'update'])
    requirements_parser.set_defaults(func=requirements_function)
    

def parse_arguments(argv, frameworks):


    """TODO: refactor this function. Maybe generate parsers and arguments based on dicts?"""
    #frameworks = functions.get_supported_frameworks(frameworks)
    framework_str = ""
    for framework in frameworks:
        framework_str += f"{framework.split('.')[1]}, "

    epilog = f"""

Supported Frameworks:
{framework_str}

"""
    parser = argparse.ArgumentParser(description="Project Creation and Management Tool.", epilog=epilog)
    subparsers = parser.add_subparsers(help='sub-command help')

    create_parser = subparsers.add_parser('create', help='create new projects')
    create_subparser = create_parser.add_subparsers(help='create sub-command help')
    create_parser.add_argument('projectname', type=str)
    create_parser.set_defaults(func=create_base_project)
    
    add_language_subparser(frameworks, create_subparser)

    add_documentation_subparser(subparsers)

    git_parser = subparsers.add_parser('git', help='git related commands')
    git_parser.add_argument('command', type=str, choices=['status', 'push'])
    git_parser.set_defaults(func=git_function)

    namespace = parser.parse_args(argv) 
    print(namespace)
    return namespace
