#!/usr/bin/env python3
import jinja2, os

def initialise_environment(project):
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('project', 'templates'),
        autoescape=jinja2.select_autoescape(['html', 'htm', 'xml'])
    )
    env.globals['name'] = project.name
    return env

def render_template(template_name, project):
    os.chdir("/Users/fabianvolkers/Developer/project-cli")
    env = initialise_environment(project)
    supported_templates = get_supported_templates('templates')
    try:
        framework = project.framework
    except AttributeError:
        framework = project.language
    if template_name in supported_templates[framework]:
        print("template found")
        template = env.get_template(f"{framework}/{template_name}.jinja2")
    elif template_name == "README.md":
        template = env.get_template("README.md.jinja2")
    else:
        print(f"template {template_name} not found in templates/{framework}")
       
    variables = get_template_variables(project)

    return template.render(project.__dict__)

def get_supported_templates(directory):
    supported_templates = {}
    try:

        if directory[0] == "/":
            full_path = directory
        else:    
            full_path = f"{os.getcwd()}/project/{directory}"

        template_dir = os.listdir(full_path)
        for subdir in template_dir:
            path = f"{full_path}/{subdir}"
            extension = subdir.split(".")[len(subdir.split("."))-1]
            if not os.path.isfile(path):
                tmp = get_supported_templates(path)
                for key in tmp:
                    try:
                        supported_templates[subdir].append(tmp[key])
                    except KeyError:
                        supported_templates[subdir] = [tmp[key]]
            elif extension == "jinja2":
                try:
                    supported_templates[directory].append(subdir.replace(".jinja2", ""))
                except KeyError:
                    supported_templates[directory] = [subdir.replace(".jinja2", "")]
    except NotADirectoryError:
        pass
            
    for framework in supported_templates:
        if type(supported_templates[framework][0]) == list:
            supported_templates[framework] = supported_templates[framework][0]
        else:
            continue

            
    return supported_templates

def get_template_variables(project):
    return project.__dict__
    for key in project.__dict__:
        print(key, project.__dict__[key])

if __name__ == "__main__":
    print(get_supported_templates("templates"))
    project = models.Project("template-test")
    get_template_variables(project)