from parser import parse_args, help_option
import sys
from registry import PathManager
import re
import os
from registry import remove_non_existing_user_paths, remove_non_existing_system_paths, get_non_existing_user_paths, get_non_existing_system_paths
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk



CALLING_DIRECTORY = os.getcwd()

def fix_flags(flags:list[str]) -> list[str]:
    retv = []
    for flag in flags:
        if flag == "--system":
            retv.append("-s")
        elif flag == "--user":
            retv.append("-u")
    return retv



def _clean_path(path:str) -> str:
    indices = len(path) - 1
    
    # if the path is just a single character
    if indices == 0:
        # dot path 
        if path[0] == ".":
            return CALLING_DIRECTORY
        # / or \ path given
        elif path[0] == "/" or path[0] == "\\":
            return __file__.split(":")[0] + ":\\"
        elif path[0] == "~":
            return os.path.expanduser("~")
        return path
    else:
        # virtual path
        # `\\wsl2$\\Ubuntu-20.04\\bin`
        if path.startswith("\\\\"):
            return path
        # relative path
        # ` \project\bin `
        elif path.startswith("\\"):
            return os.path.join(CALLING_DIRECTORY, path)
        # realtive path ' project\bin '
        elif path.startswith("\\") == False and "\\" in path:
            return os.path.join(CALLING_DIRECTORY, path)
        
        path = path.replace("/", "\\")
        
        if "\\" not in path:
            return os.path.join(CALLING_DIRECTORY, path)
        
    return path
        

def _add_helper(args:list[str], flags):
    return [_clean_path(arg) for arg in args]

def add_option(args:list[str]=[], flags:list[str]=[]) -> None:
    """add a path to the PATH environment variable

    Args:
        args (list[str], optional): _description_. Defaults to None.
        flags (list[str], optional): _description_. Defaults to None.
    """
    flags = fix_flags(flags)
    args = _add_helper(args, flags)
    pathman = PathManager()
    if "-s" in flags:
        for arg in args:
            pathman.add_system_path(arg)
    if "-u" in flags:
        for arg in args:
            pathman.add_user_path(arg)
    if "-s" not in flags and "-u" not in flags:
        for arg in args:
            pathman.add_system_path(arg)
            pathman.add_user_path(arg)
    

def list_option(args:list[str]=[], flags:list[str]=[]) -> None:
    pathman = PathManager()
    flags = fix_flags(flags)
    if "-s" in flags:
        print("system paths:")
        for p in pathman.get_system_paths():
            print("  ", p)
            
    if "-u" in flags:
        print("user paths:")
        for p in pathman.get_user_paths():
            print("  ", p)
    
    if "-s" not in flags and "-u" not in flags:
        print("system paths:")
        for p in pathman.get_system_paths():
            print("  ", p)
        print("user paths:")
        for p in pathman.get_user_paths():
            print("  ", p)
         
def remove_option(args:list[str]=[], flags:list[str]=[]) -> None:
    flags = fix_flags(flags)
    if "-s" in flags:
        pathman = PathManager()
        for arg in args:
            pathman.remove_system_path(arg)
    if "-u" in flags:
        pathman = PathManager()
        for arg in args:
            pathman.remove_user_path(arg)
    if "-s" not in flags and "-u" not in flags:
        pathman = PathManager()
        for arg in args:
            pathman.remove_system_path(arg)
            pathman.remove_user_path(arg)

def clean_option(args:list[str]=[], flags:list[str]=[]) -> None:
    flags = fix_flags(flags)
    # doesnt accept any arguments
    if "-u" in flags:
        pathman = PathManager()
        nonexists = get_non_existing_user_paths()
        for item in nonexists:
            print(f"[DOES NOT EXIST] {item}")
            pathman.remove_user_path(item)
            print(f"[REMOVED] {item}")
        remove_non_existing_user_paths()
    
    if "-s" in flags:
        pathman = PathManager()
        nonexists = get_non_existing_system_paths()
        for item in nonexists:
            print(f"[DOES NOT EXIST] {item}")
            pathman.remove_system_path(item)
            print(f"[REMOVED] {item}")
        
    if "-s" not in flags and "-u" not in flags:
        pathman = PathManager()
        nonexists = get_non_existing_system_paths()
        for item in nonexists:
            print(f"[DOES NOT EXIST] {item}")
            pathman.remove_system_path(item)
            print(f"[REMOVED] {item}")
        nonexists = get_non_existing_user_paths()
        for item in nonexists:
            print(f"[DOES NOT EXIST] {item}")
            pathman.remove_user_path(item)
            print(f"[REMOVED] {item}")

def get_option(args:list[str]=[], flags:list[str]=[]) -> None:
    flags = fix_flags(flags)
    if "-s" in flags:
        pathman = PathManager()
        print(pathman.get_system_paths())
    if "-u" in flags:
        pathman = PathManager()
        print(pathman.get_user_paths())
    if "-s" not in flags and "-u" not in flags:
        pathman = PathManager()
        print(pathman.get_system_paths())
        print(pathman.get_user_paths())

def audit_option(args:list[str]=[], flags:list[str]=[]) -> None:
    flags = fix_flags(flags)
    pathman = PathManager()
    if "-s" in flags:
        for p in pathman.get_system_paths():
            if os.path.exists(p) == False:
                print(f"[\033[34mSYSTEM\033[0m][\033[31mBROKEN\033[0m] {p}")
            else:
                print(f"[\033[34mSYSTEM\033[0m][\033[32mVALID\033[0m] {p}")
    if "-u" in flags:
        for p in pathman.get_user_paths():
            if os.path.exists(p) == False:
                print(f"[\033[34mUSER\033[0m][\033[31mBROKEN\033[0m] {p}")
            else:
                print(f"[\033[34mUSER\033[0m][\033[32mVALID\033[0m] {p}")
    if "-s" not in flags and "-u" not in flags:
        for p in pathman.get_system_paths():
            if os.path.exists(p) == False:
                print(f"[\033[34mSYSTEM\033[0m][\033[31mBROKEN\033[0m] {p}")
            else:
                print(f"[\033[34mSYSTEM\033[0m][\033[32mVALID\033[0m] {p}")
        for p in pathman.get_user_paths():
            if os.path.exists(p) == False:
                print(f"[\033[34mUSER\033[0m][\033[31mBROKEN\033[0m] {p}")
            else:
                print(f"[\033[34mUSER\033[0m][\033[32mVALID\033[0m] {p}")

def browse():
    
    def bcallback(c, d):
        root.destroy()
        if c == "exit":
            exit()
        elif c == "add all":
            add_option(d, [])
        elif c == "remove all":
            remove_option(d, [])
        elif c == "add system path":
            add_option(d, ["-s"])
        elif c == "add user path":
            add_option(d, ["-u"])
        elif c == "remove system path":
            remove_option(d, ["-s"])
        elif c == "remove user path":
            remove_option(d, ["-u"])
        
        exit()
        
    
    root = tk.Tk()
    dirname = filedialog.askdirectory(parent=root,initialdir=CALLING_DIRECTORY, title='Please select a directory')
    label = ttk.Label(root, text=dirname)
    label.pack(padx=20, pady=20)
    label2 = ttk.Label(root, text="click a button below:")
    label2.pack(padx=20, pady=20)
    
    for cmd in ["add","remove"]:
        button = ttk.Button(root, text=cmd + " system path", command=lambda: bcallback(cmd, dirname))
        button.pack(padx=20, pady=20)
        button = ttk.Button(root, text=cmd + " user path", command=lambda: bcallback(cmd, dirname))
        button.pack(padx=20, pady=20)
        button = ttk.Button(root, text=cmd + " all", command=lambda: bcallback(cmd, dirname))
        button.pack(padx=20, pady=20)

    button = ttk.Button(root, text="exit", command=lambda: bcallback("exit", dirname))
    button.pack(padx=20, pady=20)

    root.mainloop()
    
    
    return dirname

       
    
def main():
    option, args, flags = parse_args()
    
    match option:
        case "help":
            help_option(args, flags)
        case "add":
            add_option(args, flags)
        case "list":
            list_option(args, flags)
        case "remove":
            remove_option(args, flags)
        case "get":
            get_option(args, flags)
        case "clean":
            clean_option(args, flags)
        case "audit":
            audit_option(args, flags)
        case "browse":
            browse()
        case _:
            help_option(args, flags)
        
    



if __name__ == "__main__":
    main()