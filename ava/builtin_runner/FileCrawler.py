import os

class FileCrawler(object):
    def __init__(self):
        super(FileCrawler, self).__init__()
        self.root_dirs = []

        self.root_dirs.append(os.path.abspath(os.sep))

    @staticmethod
    def _is_exe(filepath):
        if (os.name == 'nt') :
            if (filepath.rpartition('.')[2] != 'exe' and filepath.rpartition('.')[2] != 'com'):
                return False
        return os.path.isfile(filepath) and os.access(filepath, os.X_OK)


    def _find(self, name, path, target_xright):
        for root, dirs, files in os.walk(path):
            for filename in files :
                if filename.upper() == name.upper() or filename.upper().rpartition('.')[0] == name.upper():
                    filepath = os.path.join(root, filename)
                    if (self._is_exe(filepath) == target_xright):
                        return filepath

    def find(self, target, target_xright = True):
        for path in self.root_dirs:
            result = self._find(target, path, target_xright)
            if (result is not None) :
                return result
        return None
