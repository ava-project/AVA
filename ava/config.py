import json
import os
from .utils import Singleton

class ConfigLoader(metaclass=Singleton):
    """
    ConfigLoader is a class that can be used for read json file
    and get prooperty easily. For now it can load only one file
    but will be extend to load multiple file.
    """

    def __init__(self, root_path):
        """
        Initializer

            @param root_path: path to the root folder of your project
            @type root_path: string
        """
        self.root_path = root_path
        self._file_loaded = None

    def load(self, path):
        """
        Load the config file

            @param path: path to the config file (relative to the root path)
            @type path: string
            @exception: OSError if the file can't be open
        """
        full_path = self.resolve_path_from_root(path)
        with open(full_path) as ofile:
            self._file_loaded = json.load(ofile)

    def get(self, path):
        """
        Get a property from the json file. If the property is inside an object,
        use the separator '/' to access. (example: path/to/my/property)

            @param path: path to the property
            @type path: string
            @exception: KeyError if the path to the property is incorrect
            @return: The property
        """
        properties = path.split('/')
        prop = None
        for key in properties:
            if prop is not None:
                prop = prop[key]
            prop = self._file_loaded[key]

        return prop

    def resolve_path_from_root(self, *path):
        """
        Append the different path to the root path.

            @param path: path to append
            @type path: list of string
            @return: The full path
            @rtype: string
        """
        return os.path.normpath(os.path.join(self.root_path, *path))
