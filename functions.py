#!/usr/bin/env python3
import os, sys, subprocess, inspect, re
import parse_args
import project as base

"""TODO: refactor every command to use subprocess"""
def get_supported_frameworks(frameworks):
    supported_frameworks = {}
    imports = inspect.getmembers(frameworks)
    for name, module in imports:
        if inspect.ismodule(module):
            for class_name, class_obj in inspect.getmembers(module):
                if inspect.isclass(class_obj):
                   
                    language_name = name
                    create_func = f"create_{language_name}_project"
                    
                    if str(class_obj) == str(base.Project):
                        language_name = "nolang"
                        create_func = "create_base_project"

                    if not hasattr(supported_frameworks, f"{language_name}.{class_obj.label}"):
                        supported_frameworks[f"{language_name}.{class_obj.label}"] = {
                            "class": class_obj,
                            "lang": language_name,
                            "create_func": getattr(parse_args, create_func)
                        }
                    
    return supported_frameworks
    

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

