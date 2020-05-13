from project import functions, frameworks, parse_args
import sys, os

def start_command():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.path.insert(0, f"{os.getcwd()}/project")
        print("Development Environment")
        #print(project)
    else:
        try:
            supported_frameworks = functions.get_supported_frameworks(frameworks)
            if len(sys.argv) == 1:
                sys.argv.append("-h")
            arguments = parse_args.parse_arguments(sys.argv[1:], supported_frameworks)
            arguments.func(arguments)
        except KeyboardInterrupt:
            sys.exit()

