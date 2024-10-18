import argparse
import textwrap 
import sys



parser = argparse.ArgumentParser(
    prog="path", 
    description="Manage the PATH(s) environment variable(s) for the current user and system",
    epilog="Use 'path help' to get help on a specific command"
)

commands = parser.add_subparsers(dest="commands")

helpParser = commands.add_parser(
    "help",
    help="Get help on a command",
    description="path help <command>",
)

helpOptions = ["add", "list", "remove", "get", "clean", "help"]
for option in helpOptions:
    helpParser.add_argument(option, action="store", nargs="?",  help=f"Get help on the {option} command")

listParser = commands.add_parser("list", description="List all paths", argument_default=None)
listParser.add_argument("-u", "--user", action="store_true", help="List the user PATH environment variable")
listParser.add_argument("-s", "--system", action="store_true", help="List the system PATH environment variable")


removeParser = commands.add_parser("remove", description="Remove a path")
removeParser.add_argument("-u", "--user", action="store_true", help="Remove the path from the user PATH environment variable")
removeParser.add_argument("-s", "--system", action="store_true", help="Remove the path from the system PATH environment variable")


addParser = commands.add_parser("add", description="Add a path")
addParser.add_argument("-s", "--system", action="store_true", help="Add the path to the system PATH environment variable")
addParser.add_argument("-u", "--user", action="store_true", help="Add the path to the user PATH environment variable")

getParser = commands.add_parser("get", description="Get paths")
getParser.add_argument("-u", "--user", action="store_true", help="Get the user PATH environment variable")
getParser.add_argument("-s", "--system", action="store_true", help="Get the system PATH environment variable")

cleanParser = commands.add_parser("clean", description="Clean all paths, remove unfindable paths")
cleanParser.add_argument("-u", "--user", action="store_true", help="Clean the user PATH environment variable")
cleanParser.add_argument("-s", "--system", action="store_true", help="Clean the system PATH environment variable")

auditParser = commands.add_parser("audit", description="Audit all paths")
auditParser.add_argument("-u", "--user", action="store_true", help="Audit the user PATH environment variable")
auditParser.add_argument("-s", "--system", action="store_true", help="Audit the system PATH environment variable")

browseParser = commands.add_parser("browse", description="Browse for paths")



all_commands = ["list", "remove", "add", "get", "clean"]
all_flags = ["-u", "-s"]
usage = "path <command> [<args>]"


def format_columns(options, descriptions, col_width=30, desc_width=50):
    result = []
    for opt, desc in zip(options, descriptions):
        # Format the options (left column)
        opt_col = textwrap.fill(opt, width=col_width)
        # Format the descriptions (right column)
        desc_col = textwrap.fill(desc, width=desc_width)
        # Combine them into one row
        result.append(f"{opt_col:<{col_width}} {desc_col}")
    return "\n".join(result)


def help_option(args:list=[], flags:list=[]):
    print(parser.prog)
    print("\nDescription:\n    " + parser.description)
    print("Usage:\n   ", usage)
    print("\nCommands:")
    desc = [cmd.description for cmd in commands.choices.values()]
    options = ["    " + cmd for cmd in commands.choices.keys()]
    print(format_columns(options, desc))
    print("")
    if "add" in args:
        print("Help on add:")
        print("    path add .my_directory           add a directory in the current working directory to both paths")
        print("\n    path add -s c:\\path\\to\\a\\thing\n    Add the path to the system PATH environment variable")
        print("    path add -u c:\\path\\to\\a\\thing\n    Add the path to the user PATH environment variable")
    if "list" in args:
        print("Help on list:\n    path list -s\n    List the system PATH environment variable")
        print("    path list -u\n    List the user PATH environment variable")
    if "remove" in args:
        print("Help on remove:\n    path remove -s c:\\path\\to\\a\\thing\n    Remove the path from the system PATH environment variable")
        print("    path remove -u c:\\path\\to\\a\\thing\n    Remove the path from the user PATH environment variable")
    if "get" in args:
        get_Extra = """
        just like list, will print out the paths in the system PATH environment variable 
        but allows you to get the user PATH environment as json / xml / bytes / .pickle
        """
        print("Help on get:\n    path get -s\n    Get the system PATH environment variable")
        print("    path get -u\n    Get the user PATH environment variable")
    if "clean" in args:
        print("Help on clean:")
        print("""\
    the clean command goes through all the PATH environment variables
    and removes any paths that are not found on your system.
    this does not include %<NAME>% variables.
              """)
        print("    path clean -s\n    Clean the system PATH environment variable")
        print("    path clean -u\n    Clean the user PATH environment variable")
    
    if "audit" in args:
        print("Help on audit:")
        print("    path audit -s\n    Audit the system PATH environment variable")
        print("    path audit -u\n    Audit the user PATH environment variable")
    
    if "browse" in args:
        print("Help on browse:")
        print("    path browse\n    Browse for paths")
    


        
def parse_args() -> tuple[str, list, list]:
    command = parser.parse_args().commands
    sys.argv.append(None)
    args = sys.argv[sys.argv.index(command):]
    sys.argv.pop(-1)
    args.pop(0)
    flags = []
    for arg in args:
        if arg.startswith("-"):
            flags.append(arg)
    args = [arg for arg in args if arg not in flags]
    
    return command, args, flags

def test(*args):
    import sys
    sys.argv.extend(args)
    print("args: ", sys.argv)
    namespace = parse_args()
    print(namespace)
    sys.argv.pop(-1)

def testall():
    print_help()
    input("...")
    for cmd in all_commands:
        test(cmd)

