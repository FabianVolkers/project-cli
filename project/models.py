#!/usr/bin/env python3

#import frameworks, parse_args, functions
#from project import functions
import project.functions as functions
import project.template as template
#import .functions as functions
import os, sys, re


class Meta(type):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        """TODO: add negative lookbehind for regex project not at start of string"""
        if name == "Project":
            label = name
        else:
            label_re = re.compile("Project|JS")
            label = re.sub(label_re, "", name)
            
        x.label = label.lower()
        return x
    

class Project(metaclass=Meta):
    def __init__(self, name, branch='master', remote='origin'):
        self.name = name
        self.branch = branch
        self.remote = remote
    

    def __repr__(self):
        return f"""
Name:\t\t {self.name}
"""


    def initialise(self):
        dev_dir = functions.get_dev_dir()
        self.name, dev_dir = functions.validate_name(self.name, dev_dir)
        self.create_dir(dev_dir)
        self.initialise_git()
        #self.initialise_github()
        self.create_readme()
        self.save_to_file()


    def create_dir(self, parent_directory):

        self.path = f"{parent_directory}/{self.name}"
        try:
            os.mkdir(self.path, 0o744)
            os.chdir(self.path)
            print(f"Created project directory at {self.path}")
        except FileExistsError:
            print(f"Error creating directory, {self.path} already exists.")
            self.path = None
            sys.exit()
        except PermissionError:
            print(f"Permission denied. Make sure your user can access {parent_directory}.")
        

    def initialise_git(self, branch='master'):
        #TODO: refactor to use git-flow cli tool
        stdout, stderr, returncode = functions.run_process("git init")

        if returncode == 0:
            self.repo_name = self.name
            self.branch = branch
            print(stdout)
            return True
            
        else:
            print("Error initialising git.")
        

    def initialise_github(self, remote='origin'):

        stdout, stderr, returncode = functions.run_process(f"gh repo create {self.repo_name}")

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
        os.chdir(self.path)
        stdout, stderr, returncode = functions.run_process(f"git add {filename}")
        if returncode == 0:
            print(stdout)
            stdout, stderr, returncode = functions.run_process(f"git commit -m '[project cli] generate {filename}'")
            if returncode == 0:
                print(stdout)
                stdout, stderr, returncode = functions.run_process(f"git push {self.remote} {self.branch}")
                if returncode == 0:
                    print(stdout)
                else:
                    print(stdout, stderr, returncode)
            else:
                print(stdout, stderr, returncode)
        else:
            print(stdout, stderr, returncode)

    def create_readme(self):
        filename = "README.md"
        self.readme = f"{self.path}/{filename}"
        functions.create_file_from_template(self.readme, self, filename)
        #self.push_file_to_remote(filename)
        

    def save_to_file(self):
        with open(f'{self.path}/.project', 'w') as file:
            file.write(f"class={self.__class__}\n")
            newline_chr = "\n"
            newline_str = "\\n"
            for attribute in self.__dict__.keys():
                file.write(f"{attribute}={str(self.__dict__[attribute]).replace(newline_chr, newline_str)}\n")
            file.close()
    
    def load(self, attributes):    
        for attribute in attributes:
            key, value = attribute.split("=")
            setattr(self, key, value)


if __name__ == "__main__":
    try:
        supported_frameworks = functions.get_supported_frameworks(frameworks)
        arguments = parse_args.parse_arguments(sys.argv[1:], supported_frameworks)
        arguments.func(arguments)
    except KeyboardInterrupt:
        sys.exit()

