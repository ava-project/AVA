import os


class FileCrawler(object):
    def __init__(self):
        super(FileCrawler, self).__init__()
        self.Treshold_restraint = 100
        self.root_dirs = [
            str(os.path.expanduser('~')),
            str(os.environ.get("ProgramFiles")),
            str(os.environ.get("ProgramW6432")),
            str(os.getenv('APPDATA')),
            str('/usr/bin'),
            str('/usr/sbin'),
            "/Applications"
        ]
        for user_dirs, user_sub_dirs, files in os.walk(os.path.expanduser('~')):
            for name in user_sub_dirs:
                if (name[0] != '.'):
                    self.root_dirs.append(os.path.join(user_dirs, name))
            break

    @staticmethod
    def _is_exe(filepath):
        import platform
        if os.name == 'nt':
            if (filepath.rpartition('.')[2] != 'exe' and filepath.rpartition('.')[2] != 'com'):
                return False
        elif os.name == 'posix' and platform.system() == 'Darwin':
            print(os.path.isfile(filepath))
            print(os.access(filepath, os.X_OK))
            if filepath.rpartition('.')[2] == 'app':
                return True
        return os.path.isfile(filepath) and os.access(filepath, os.X_OK)

    def _find(self, name, path, target_xright, level):
        path_size = max(len(path.rsplit('\\')), len(path.rsplit('/')))
        autocount = 0
        result = None
        for root, dirs, files in os.walk(path):
            autocount += 1
            current_size = max(len(root.rsplit('\\')), len(root.rsplit('/')))
            current_level = current_size - path_size
            """
                to shorten the search, if we are iterating a large amount of
                dirs, we stay at level 0
            """
            if (autocount >= self.Treshold_restraint):
                if (root.upper().find(name.upper()) == -1):
                    level = 0
                else:
                    print(root)
                    if (target_xright is False):
                        result = root
                    level = 4

            if (current_level > level):
                dirs[:] = []
                files[:] = []
                # break;
            """
                if we're not looking for a file (. extension) or something
                executable we might want to return a directory
            """
            if (target_xright is False and len(name.rsplit('.')) < 2):
                for dirname in dirs:
                    if (dirname.upper() == name.upper()):
                        return os.path.join(path, dirname)
            """
                we try the files
            """
            for filename in files:
                if filename.upper() == name.upper() or filename.upper().rpartition('.')[0] == name.upper():
                    filepath = os.path.join(root, filename)
                    if (target_xright is True and self._is_exe(filepath)):
                        return filepath
                    if (target_xright is False):
                        return filepath
        return result

    def find(self, target, target_xright=True):
        level = 0
        """
            First we test direclty the subdirs containing [target] in their
            name in order to speed up the research
        """
        for path in self.root_dirs:
            for x in os.walk(path):
                for d in x[1]:
                    if d.upper().find(target.upper()) > -1:
                        newpath = os.path.join(path, d)
                        result = self._find(target, newpath, target_xright, level)
                        if (result is not None):
                            return result
                break
            level = 4
        """
            If we didnt find it first, we try the roots dirs entirely
        """
        level = 0

        for path in self.root_dirs:
            result = self._find(target, path, target_xright, level)
            if (result is not None):
                return result
            level = 4
        return None
