import os
import winreg


KEY1 = (winreg.HKEY_CURRENT_USER, "Environment")
KEY2 = (
    winreg.HKEY_LOCAL_MACHINE,
    "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",
)
PATH1 = (winreg.HKEY_CURRENT_USER, "Environment", "Path")
PATH2 = (
    winreg.HKEY_LOCAL_MACHINE,
    "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",
    "Path",
)
TYPE1 = winreg.REG_EXPAND_SZ
TYPE2 = winreg.REG_EXPAND_SZ


def expand_string(string: str) -> str:
    """Expands a string containing environment variable references.

    If the string contains one or more substrings of the form %envar%,
    then each such substring is replaced by the value of the environment
    variable ``envar`` if it exists, otherwise the original substring is
    left unchanged. If ``envar`` is the string "PATH", then the substring
    is left unchanged. The returned string is the original string with all
    such substrings replaced.

    Parameters
    ----------
    string : str
        The string to expand.

    Returns
    -------
    str
        The expanded string.
    """
    if string.startswith("%"):
        end = string.rindex("%")
        start = string.index("%")
        envar = string[start + 1 : end].strip("%")
        if envar == "PATH":
            return string
        p = os.environ[envar]
        print(envar, " <--", p)
        return p + string[end + 1 :]
    else:
        return string


def get_path_variable(system=True) -> list[str]:
    """Returns the PATH environment variable as a list of strings.

    If `system` is ``True`` (the default), the system-wide PATH is returned.
    If `system` is ``False``, the user-specific PATH is returned.

    Any substrings of the form %envar% are expanded to the value of the
    environment variable ``envar`` if it exists, otherwise the original
    substring is left unchanged. If ``envar`` is the string "PATH", then the
    substring is left unchanged.

    Parameters
    ----------
    system : bool, optional
        Whether to return the system-wide PATH (the default) or the
        user-specific PATH.

    Returns
    -------
    list[str]
        The expanded PATH environment variable as a list of strings.
    """
    if system == False:
        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH1[2])
            value = value.split(";")
            return value

    elif system == True:
        with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH2[2])
            value: list[str] = value.split(";")
            v = []
            for val in value:
                if val[1] == "%PATH%":
                    continue
                else:
                    v.append(val)
        return v


def add_to_user_path(path: str) -> None:
    """Adds a path to the user's PATH environment variable.

    Parameters
    ----------
    path : str
        The path to add to the user's PATH environment variable.

    Returns
    -------
    None
    """
    strings = get_path_variable(system=False)
    strings.append(path)
    strings = ";".join(strings)

    with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
        winreg.SetValueEx(key, PATH1[2], 0, TYPE1, strings)
        winreg.FlushKey(key)


def add_to_system_path(path: str) -> None:
    """Adds a path to the system-wide PATH environment variable.

    Parameters
    ----------
    path : str
        The path to add to the system-wide PATH environment variable.

    Returns
    -------
    None
    """
    strings = get_path_variable(system=True)
    strings.append(path)
    strings = ";".join(strings)

    with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
        winreg.SetValueEx(key, PATH2[2], 0, TYPE2, strings)
        winreg.FlushKey(key)


def remove_from_user_path(path: str) -> None:
    """Removes a path from the user's PATH environment variable.

    Parameters
    ----------
    path : str
        The path to remove from the user's PATH environment variable.

    Returns
    -------
    None
    """
    strings = get_path_variable(system=False)
    strings.remove(path)
    strings = ";".join(strings)

    with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
        winreg.SetValueEx(key, PATH1[2], 0, TYPE1, strings)
        winreg.FlushKey(key)


def remove_from_system_path(path: str) -> None:
    """Removes a path from the system-wide PATH environment variable.

    Parameters
    ----------
    path : str
        The path to remove from the system-wide PATH environment variable.

    Returns
    -------
    None
    """
    strings = get_path_variable(system=True)
    strings.remove(path)
    strings = ";".join(strings)

    with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
        winreg.SetValueEx(key, PATH2[2], 0, TYPE2, strings)
        winreg.FlushKey(key)


def remove_paths_from_system_path(paths: list[str]) -> None:
    """Removes multiple paths from the system-wide PATH environment variable.

    Parameters
    ----------
    paths : list[str]
        A list of paths to remove from the system-wide PATH environment variable.

    Returns
    -------
    None
    """
    strings = get_path_variable(system=True)
    for path in paths:
        strings.remove(path)
    strings = ";".join(strings)

    with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
        winreg.SetValueEx(key, PATH2[2], 0, TYPE2, strings)
        winreg.FlushKey(key)


def remove_paths_from_user_path(paths: list[str]) -> None:
    """Removes multiple paths from the user-wide PATH environment variable.

    Parameters
    ----------
    paths : list[str]
        A list of paths to remove from the user-wide PATH environment variable.

    Returns
    -------
    None
    """
    strings = get_path_variable(system=False)
    for path in paths:
        strings.remove(path)
    strings = ";".join(strings)

    with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
        winreg.SetValueEx(key, PATH1[2], 0, TYPE1, strings)
        winreg.FlushKey(key)


def add_to_path(path: str, system=True) -> None:
    """Adds a path to the PATH environment variable.

    Parameters
    ----------
    path : str
        The path to add to the PATH environment variable.
    system : bool, optional
        If True, the path is added to the system-wide PATH environment variable.
        If False, the path is added to the user-wide PATH environment variable.
        Defaults to True.

    Returns
    -------
    None
    """
    strings = get_path_variable(system=system)
    strings.append(path)
    strings = ";".join(strings)

    if system == False:
        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            winreg.SetValueEx(key, PATH1[2], 0, TYPE1, strings)
            winreg.FlushKey(key)
    elif system == True:
        with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
            winreg.SetValueEx(key, PATH2[2], 0, TYPE2, path)
            winreg.FlushKey(key)


def get_non_existing_paths() -> list[tuple[str, str]]:
    """
    Retrieves a list of non-existing paths from the system and user PATH environment variables.

    This function checks both the system-wide and user-specific PATH environment variables
    for paths that do not exist on the file system. If a path is not found, it attempts to
    expand any environment variable placeholders in the path and checks again. Non-existing
    paths are categorized as either "SYSTEM" or "USER" based on their origin.

    Returns
    -------
    list[tuple[str, str]]
        A list of tuples, where each tuple contains a string indicating the path's origin
        ("SYSTEM" or "USER") and the non-existing path itself.
    """
    system_paths = get_path_variable(system=True)
    user_paths = get_path_variable(system=False)
    retv = []
    for path in system_paths:
        if os.path.exists(path) == False:
            expanded = expand_string(path)
            if os.path.exists(expanded):
                continue
            else:
                retv.append(["SYSTEM", path])
                continue

    for path in user_paths:
        if os.path.exists(path) == False:
            expanded = expand_string(path)
            if os.path.exists(expanded):
                continue
            else:
                retv.append(["USER", path])

    return retv


def get_non_existing_user_paths() -> list[str]:
    """
    Retrieves a list of non-existing user-specific paths from the PATH environment variable.

    This function checks the user-specific PATH environment variable for paths
    that do not exist on the file system. If a path is not found, it attempts to
    expand any environment variable placeholders in the path and checks again.
    Non-existing paths are collected and returned.

    Returns
    -------
    list[str]
        A list of non-existing paths from the user-specific PATH environment variable.
    """
    user_paths = get_path_variable(system=False)
    retv = []

    for path in user_paths:
        if os.path.exists(path):
            continue

        expanded = expand_string(path)
        if os.path.exists(expanded):
            continue

        retv.append(path)

    return retv


def get_non_existing_system_paths() -> list[str]:
    """
    Retrieves a list of non-existing system-wide paths from the PATH environment variable.

    This function checks the system-wide PATH environment variable for paths that do not exist on the file system. If a path is not found, it attempts to expand any environment variable placeholders in the path and checks again. Non-existing paths are collected and returned.

    Returns
    -------
    list[str]
        A list of non-existing paths from the system-wide PATH environment variable.
    """
    system_paths = get_path_variable(system=True)
    retv = []
    for path in system_paths:
        if os.path.exists(path):
            continue
        expanded = expand_string(path)
        if os.path.exists(expanded):
            continue

        retv.append(path)

    return retv


def remove_non_existing_user_paths():
    """
    Removes non-existing user-specific paths from the PATH environment variable.

    This function retrieves a list of non-existing user-specific paths from the PATH environment variable
    and iterates through each path, removing it from the PATH variable.

    Returns
    -------
    None
    """
    non_existing = get_non_existing_user_paths()

    for item in non_existing:
        print(f"removing {item}")
        remove_from_user_path(item)


def remove_non_existing_paths():
    """
    Removes non-existing paths from both the system-wide and user-specific PATH environment variables.

    This function retrieves a list of non-existing paths from both the system-wide and user-specific PATH environment variables
    and iterates through each path, removing it from the appropriate PATH variable.

    Returns
    -------
    None
    """
    non_existing = get_non_existing_paths()
    for item in non_existing:
        if item[0] == "SYSTEM":
            remove_from_system_path(item[1])
        elif item[0] == "USER":
            remove_from_user_path(item[1])


def remove_non_existing_system_paths():
    """
    Removes non-existing system-wide paths from the PATH environment variable.

    This function retrieves a list of non-existing system-wide paths from the PATH environment variable
    and iterates through each path, asking the user for confirmation before removing it from the PATH variable.

    Returns
    -------
    None
    """

    paths = get_non_existing_system_paths()

    for path in paths:
        remove_from_system_path(path)
        


class PathManager:
    def __init__(self) -> None:
        self.domain = {"System", "User"}

    def user_path(self):
        """Returns the user-specific PATH environment variable value"""

        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH1[2])
            return value

    def system_path(self):
        """Returns the system PATH environment variable value"""

        try:
            with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
                value, type = winreg.QueryValueEx(key, PATH2[2])
                return value
        except:
            None

    def get_user_paths(self) -> list[str]:
        """Returns the PATH environment variable values"""

        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH1[2])
            value = value.split(";")
            return value

    def get_system_paths(self) -> list[str]:
        """Returns the PATH environment variable values"""

        with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH2[2])
            value: list[str] = value.split(";")
            v = []
            for val in value:
                if val[1] == "%PATH%":
                    continue
                else:
                    v.append(val)

        return v

    def add_user_path(self, path: str) -> None:
        """Adds a path to the user-specific PATH environment variable."""
        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH1[2])

        value = value.split(";")

        for val in value:
            if value == path:
                return

        value.append(path)
        value = ";".join(value)

        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            winreg.SetValueEx(key, PATH1[2], 0, TYPE1, value)

    def add_system_path(self, path: str) -> None:
        """Adds a path to the system-wide PATH environment variable."""

        with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH2[2])

        value = value.split(";")

        for val in value:
            if value == path:
                return

        value.append(path)
        value = ";".join(value)

        with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
            winreg.SetValueEx(key, PATH2[2], 0, TYPE2, value)

    def system_has_path(self, path: str) -> bool:
        """Returns True if the system-wide PATH environment variable contains the specified path, False otherwise."""

        with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH2[2])

        value = value.split(";")

        for val in value:
            if val == path:
                return True

        return False

    def user_has_path(self, path: str) -> bool:
        """Returns True if the user-specific PATH environment variable contains the specified path, False otherwise."""

        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH1[2])

        value = value.split(";")

        for val in value:
            if val == path:
                return True

        return False

    def remove_user_path(self, path: str):
        """Removes a path from the user-specific PATH environment variable."""
        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH1[2])

        value = value.split(";")

        for val in value:
            if val == path:
                value.remove(val)

        value = ";".join(value)

        with winreg.OpenKey(KEY1[0], KEY1[1]) as key:
            winreg.SetValueEx(key, PATH1[2], 0, TYPE1, value)

    def remove_system_path(self, path: str):
        """Removes a path from the system-wide PATH environment variable."""
        with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
            value, type = winreg.QueryValueEx(key, PATH2[2])

        value = value.split(";")

        for val in value:
            if val == path:
                value.remove(val)

        value = ";".join(value)

        with winreg.OpenKey(KEY2[0], KEY2[1]) as key:
            winreg.SetValueEx(key, PATH2[2], 0, TYPE2, value)

    def add_systemwide_path(self, path: str) -> None:
        if self.system_has_path(path) == False:
            self.add_system_path(path)
        if self.user_has_path(path) == False:
            self.add_user_path(path)

    def remove_systemwide_path(self, path: str) -> None:
        if self.system_has_path(path) == True:
            self.remove_system_path(path)
        if self.user_has_path(path) == True:
            self.remove_user_path(path)

    def list_paths(self) -> list[str]:
        system = self.get_system_paths()
        user = self.get_user_paths()
        return system + user
