
# Project CLI <!-- omit in TOC -->

A Command line tool for initialising and managing development projects. Also some basic code generation.

## Contents <!-- omit in TOC -->
- [Overview](#overview)
- [Features](#features)
    - [Support for Languageless, Python (Flask) and Javascript projects.](#support-for-languageless-python-flask-and-javascript-projects)
    - [Project initialisation including supported frameworks.](#project-initialisation-including-supported-frameworks)
    - [git and github initialisation](#git-and-github-initialisation)
    - [Readme and code generation.](#readme-and-code-generation)
    - [coming soon:](#coming-soon)
- [Usage](#usage)
- [Build with](#build-with)
- [Contributing](#contributing)

## Overview
Initialise new development projects with support for multiple frameworks and languages.

## Features
#### Support for Languageless, Python (Flask) and Javascript projects.

#### Project initialisation including supported frameworks.

#### git and github initialisation

#### Readme and code generation.

#### coming soon:
- deployment
- importing existing project
- git-flow enforcement
- Improved readme generation
- Django support (incl. rest framework)
- Django Rest Framework code generation


## Usage
```
usage: project [-h] {create,readme,requirements,git} ...

Project Creation and Management Tool.

positional arguments:
  {create,readme,requirements,git}
                        sub-command help
    create              create new projects
    readme              readme related commands
    requirements        requirements commands
    git                 git related commands

optional arguments:
  -h, --help            show this help message and exit

Supported Frameworks: javascript, node, project, vue, flask, python,

```

## Build with
- Python 3
- Jinja2

## Contributing

To add support for new languages or frameworks, the following requirements have to be fulfilled

- A new class inheriting from `models.Project`or any other class with the `models.Project` as base class
- Make sure the class is imported in `frameworks.py`

> This will automatically create an argument parser for the language.

If you implement a initialise_structure method on your framework class for code generation you can put your jinja templates in `templates/{framework}`

You can render your template by calling `functions.create_file_from_template`. The function will use `project.__dict__` as input variables.