#!/usr/bin/env python3
#import python, javascript
import os, sys, argparse, subprocess
"""TODO: refactor every command to use subprocess"""
"""TODO: refactor functions into own file"""

def confirm_action(response):
    if response == "y" or response == "yes":
        return True

    elif response == "n" or response == "no":
        return False
    else:
        response = input("Please type y or n\n")
        return confirm_action(response)

def check_full_path(path):
    if len(path) == 0 or not path[0] == "/":
        print("Please specify the full path of your project directory")
        path = input("Path: ")
        return check_full_path(path)
    else:
        if path[len(path)-1] == "/":
            path = path[:len(path)-1]

        return path

def confirm_option(response, nOptions):
    try:
        response = int(response)
    except ValueError:
        response = input(f'Please chose one of the options between 1 and {nOptions}')
        return confirm_option(response, nOptions)
    finally:
        if response > 0 and response <= nOptions:
            return response
        else:
            response = input(f'Please chose one of the options between 1 and {nOptions}')
            return confirm_option(response, nOptions)

def set_default_dev_dir():
    print("Default dev dir environment variable not set.")
    print("Please specify a default project parent directory in which to put all project directories.")
    
    dev_dir = input('Path: ')
    dev_dir = check_full_path(dev_dir)

    response = input('Do you want to store the default path in your environment variables? y|n:')
    store_env_var = confirm_action(response)

    if store_env_var:
        home = os.popen("echo $HOME").read()
        temp = os.popen("echo $SHELL").read()
        temp = temp.split("/")
        shell = temp[len(temp)-1].replace("\n", "")
        command = f'echo "\ \n \ \n# Project cli tool\ \nexport PROJECT_DEV_DIR={dev_dir}" >> "$HOME/.{shell}rc"'
        #print(command)
        os.system(command)
        os.system(f"source $HOME/.{shell}rc")

    return dev_dir


def get_dev_dir():
    try:
        dev_dir = os.environ['PROJECT_DEV_DIR']
    except KeyError:
        dev_dir = set_default_dev_dir()
    
    return dev_dir

def validate_name(name, dev_dir):
    existing_dirs = os.listdir(dev_dir)
    path = dev_dir
    if name in existing_dirs:
        print(f"The directory {dev_dir}/{name} already exists.")
        response = input("""Do you want to change
[1] The project name
[2] The project path
"""
        )
        response = confirm_option(response, 2)
        if response == 1:
            name, path = validate_name(input('Please enter a new project name: '), dev_dir)
        elif response == 2:
            name, path = validate_name(name, input('Please specify a different parent directory for the new project directory: '))

    return name, path


def run_process(command):
    process = subprocess.run(command, shell=True, capture_output=True)
    stderr = process.stderr.decode('utf-8')
    stdout = process.stdout.decode('utf-8')
    return stdout, stderr, process.returncode


class Project:
    def __init__(self, name, branch='master', remote='origin'):
        self.name = name
        self.branch = branch
        self.remote = remote
    
    def __repr__(self):
        return f"""
Name:\t\t {self.name}
"""
    def initialise(self):
        dev_dir = get_dev_dir()
        self.name, dev_dir = validate_name(self.name, dev_dir)
        self.create_dir(dev_dir)
        self.initialise_git()
        self.initialise_github()
        self.create_readme()
        self.save_to_file()

    def create_dir(self, parent_directory):

        self.path = f"{parent_directory}/{self.name}"
        try:
            os.mkdir(self.path, 0o744)
            os.chdir(self.path)
        except FileExistsError:
            print(f"Error creating directory, {self.path} already exists.")
            self.path = None
            sys.exit()
        except PermissionError:
            print(f"Permission denied. Make sure your user can access {parent_directory}.")
        

    def initialise_git(self, branch='master'):
        git = os.popen("git init").read()
        print(git)
        
        if git.find(f"Initialized empty Git repository in {self.path}/.git/") > -1:
            self.repo_name = self.name
            self.branch = branch
            return True
        else:
            print("Error initialising git.")
        

    def initialise_github(self, remote='origin'):

        stdout, stderr, returncode = run_process(f"gh repo create {self.repo_name}")

        if returncode == 0:
            self.repo_name = stdout.replace("\n", "")
            self.remote = remote
            print(f"Created new github repository {self.repo_name} and set remote {self.remote}.")
        elif stderr.find("graphql error: 'Name already exists on this account'") > -1:
            print(f"You already have an existing GitHub repo with the name {self.name}")
            print("Enter a different repo name or leave blank to continue without connecting to GitHub.")
            response = input("Repository name: ")
            if not response == "":
                self.repo_name = response
                self.initialise_github()
        else:
            print(stderr)
    
    def push_file_to_remote(self, filename):
        stdout, stderr, returncode = run_process(f"git add {filename}")
        if returncode == 0:
            print(stdout)
            stdout, stderr, returncode = run_process(f"git commit -m '[project cli] generate readme'")
            if returncode == 0:
                print(stdout)
                stdout, stderr, returncode = run_process(f"git push {self.remote} {self.branch}")
                if returncode == 0:
                    print(stdout)
                else:
                    print(stdout, stderr, returncode)
            else:
                print(stdout, stderr, returncode)
        else:
            print(stdout, stderr, returncode)

    def create_readme(self):
        self.readme = f"""

# {self.name} <!-- omit in TOC -->
This is the README for {self.name}

## Contents <!-- omit in TOC -->
- [Section 1](#section-1)

## Section 1
This readme was generated by the project cli tool.

"""
        filename = "README.md"
        try:
            with open(filename, "x") as readme_file:
                readme_file.write(self.readme)
                readme_file.close()
            self.push_file_to_remote(filename)
        except FileExistsError:
            print("readme file exists, not overwriting")

    def save_to_file(self):
        with open('.project', 'w') as file:
            for attribute in self.__dict__.keys():
                file.write(f"{attribute}={self.__dict__[attribute].encode()}\n")
            file.close()


def create_project(args):
    print(f'creating project')
    project = Project(args.projectname)
    project.initialise()
    
def create_javascript_project(args):
    print('creating javascript project')

def create_python_project(args):
    print('creating python project')

def git_function(args):
    print('git commands')

def readme_function(args):
    print('readme command')

def requirements_function(args):
    print('requirements command')

def parse_arguments(argv):
    """TODO: refactor this function. Maybe generate parsers and arguments based on dicts?"""
    parser = argparse.ArgumentParser(description='Project Creation and Management Tool.')
    subparsers = parser.add_subparsers(help='sub-command help')

    
    
    create_parser = subparsers.add_parser('create', help='create new projects')
    create_parser.add_argument('projectname', type=str)
    create_parser.set_defaults(func=create_project)
    create_subparser = create_parser.add_subparsers(help='create sub-command help')

    PYTHON_FRAMEWORKS = ['flask', 'django']
    python_parser = create_subparser.add_parser('python', help='create python projects')
    python_parser.add_argument('-f', '--framework', type=str, choices=PYTHON_FRAMEWORKS)
    python_parser.set_defaults(func=create_python_project)

    JAVASCRIPT_FRAMEWORKS = ['vue', 'angular', 'react']
    javascript_parser = create_subparser.add_parser('javascript', help='create javascript projects')
    javascript_parser.add_argument('-f', '--framework', type=str, choices=JAVASCRIPT_FRAMEWORKS)
    javascript_parser.set_defaults(func=create_javascript_project)
    
    
    git_parser = subparsers.add_parser('git', help='git related commands')
    git_parser.add_argument('command', type=str, choices=['status', 'push'])
    git_parser.set_defaults(func=git_function)

    """Maybe refactor readme and requirements into single subparser named documentation"""
    readme_parser = subparsers.add_parser('readme', help='readme related commands')
    readme_parser.add_argument('command', type=str, choices=['create', 'show', 'update'])
    readme_parser.add_argument('-g', '--git', nargs=2, type=str, help='Push updated README to git remote', metavar=('remote', 'branch'))
    readme_parser.set_defaults(func=readme_function)

    requirements_parser = subparsers.add_parser('requirements', help='requirements commands')
    requirements_parser.add_argument('command', type=str, choices=['create', 'show', 'update'])
    requirements_parser.set_defaults(func=requirements_function)
    namespace = parser.parse_args(argv) 
    print(namespace)
    return namespace

if __name__ == "__main__":

    try:
        arguments = parse_arguments(sys.argv[1:])
        arguments.func(arguments)
    except KeyboardInterrupt:
        sys.exit()


"""     dev_directory = os.environ("DEVELOPMENT_DIRECTORY")
    project = Project(name, language, framework)
    project.create_dir(dev_directory)
    project.initialise_git()
    project.initalise_github()
    project.initialise_environment()
    project.initialise_framework() """