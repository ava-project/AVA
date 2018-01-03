import os

class FileCrawler(object):
    def __init__(self):
        super(FileCrawler, self).__init__()
        # self.root_dirs = [os.path.expanduser('~\\Pictures')]
        # self.root_dirs = ['C:\\Users\\Jamais\\Documents\\Perso']
        self.root_dirs = [os.path.expanduser('~\\Pictures'),os.path.expanduser('~\\Documents'), os.path.expanduser('~\\Videos'),'C:\\Program Files', 'C:\\Program Files (x86)']
        # self.root_dirs.append(os.path.abspath(os.sep))

    @staticmethod
    def _is_exe(filepath):
        if (os.name == 'nt') :
            if (filepath.rpartition('.')[2] != 'exe' and filepath.rpartition('.')[2] != 'com'):
                return False
        return os.path.isfile(filepath) and os.access(filepath, os.X_OK)


    def _find(self, name, path, target_xright, level):
        path_size = len(path.rsplit('\\'))
        for root, dirs, files in os.walk(path) :
            current_size = len(root.rsplit('\\'))
            current_level = current_size - path_size
            if (current_level > level) :
                continue
            #### if we're not looking for a file (. extension) or something executable
            #### we might want to return a directory
            if (target_xright is False and len(name.rsplit('.')) < 2) :
                    for dirname in dirs :
                        if (dirname.upper() == name.upper()) :
                            return os.path.join(path, dirname)
            ##### we try the files
            for filename in files :
                    if filename.upper() == name.upper() or filename.upper().rpartition('.')[0] == name.upper():
                        filepath = os.path.join(root, filename)
                        print("[" + filename + "]")
                        if (target_xright is True and self._is_exe(filepath)) :
                            return filepath
                        if (target_xright is False) :
                            return filepath


    def find(self, target, target_xright = True):
        #### First we test direclty the subdirs containing [target] in their name
        ### in order to speed up the research
        for path in self.root_dirs:
            for x in os.walk(path):
                for d in x[1]:
                    if d.upper().find(target.upper()) > -1 :
                        newpath = os.path.join(path, d)
                        result = self._find(target, newpath, target_xright, 2)
                        if (result is not None) :
                            return result
                break
        #### If we didnt find it first, we try the roots dirs entirely
        for path in self.root_dirs :
            result = self._find(target, path, target_xright, 2)
            if (result is not None) :
                return result
        return None
