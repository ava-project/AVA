import json
import os
from .utils import Singleton

class ConfigLoader(metaclass=Singleton):
    """
    ConfigLoader is a class that can be used for read json file
    and get prooperty easily. For now it can load only one file
    but will be extend to load multiple file.
    """

    def __init__(self, root_path, queues):
        """
        Initializer

            @param root_path: path to the root folder of your project
            @type root_path: string
        """
        self.root_path = root_path
        self._file_loaded = None
        self._queues = queues

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

    def exist(self, path):
        return False if self.get(path) is None else True

    def get(self, path):
        """
        Get a property from the json file. If the property is inside an object,
        use the separator '/' to access. (example: path/to/my/property)

            @param path: path to the property
            @type path: string
            @exception: KeyError if the path to the property is incorrect
            @return: The property
        """
        return self._access(path)

    def _access(self, path, value=None, create=False):
        properties = path.split('/')
        psize = len(properties)
        node = None
        for i, key in zip(range(psize), properties):
            save_node = self._file_loaded if node is None else node
            node = node.get(key) if node is not None else self._file_loaded.get(key)
            if value is None:
                #get
                if node is None or not isinstance(node, dict):
                    if i != psize - 1:
                        node = None
                    break
            else:
                #set
                if i == psize - 1 and node is not None:
                    save_node[key] = value
                    node = value
                if not create:
                    if node is None or not isinstance(node, dict):
                        if i != psize - 1:
                            node = None
                        break
                else:
                    if i == psize - 1:
                        save_node[key] = value
                        node = value
                    elif node is None or not isinstance(node, dict):
                        save_node[key] = {}
                        node = save_node[key]
        return node

    def put_and_create(self, path, value):
        return self._access(path, value, True)

    def put(self, path, value):
        return self._access(path, value, False)

    def subscribe(self, component_name, path):
        self._queues['QueueComponentManager'].put('subscribe %s %s' % (component_name, path))
        return self.get(path)

    def update(self, path, value):
        self._queues['QueueComponentManager'].put('update %s %s' % (path, value))
        return self.put_and_create(path, value)

    def resolve_path_from_root(self, *path):
        """
        Append the different path to the root path.

            @param path: path to append
            @type path: list of string
            @return: The full path
            @rtype: string
        """
        return os.path.normpath(os.path.join(self.root_path, *path))