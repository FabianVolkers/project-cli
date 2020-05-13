
# Project CLI <!-- omit in TOC -->

A Command line tool for initialising and managing development projects. Also some basic code generation.

## Contents <!-- omit in TOC -->
- [Overview](#overview)
- [Features](#features)
    - [Support for Languageless, Python (Flask) and Javascript projects.](#support-for-languageless-python-flask-and-javascript-projects)
    - [Project initialisation including supported frameworks.](#project-initialisation-including-supported-frameworks)
    - [git and github initialisation](#git-and-github-initialisation)
    - [Readme generation.](#readme-generation)
    - [coming soon:](#coming-soon)
- [Usage](#usage)
- [Build with](#build-with)

## Overview
Initialise new development projects with support for multiple frameworks and languages.

## Features
#### Support for Languageless, Python (Flask) and Javascript projects.

#### Project initialisation including supported frameworks.

#### git and github initialisation

#### Readme generation.

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
Python 3
