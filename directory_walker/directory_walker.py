from os import walk
from os import path


class DirectoryWalker:

    def __init__(self):
        self._list_of_files = []
        self._list_of_dirs = []
        self._list_of_dir_files = []
        self._path_to_dir = ""
        self._list_of_json_files = []
        self._json_tuples = []

    @property
    def list_of_files(self):
        return self._list_of_files

    @list_of_files.setter
    def list_of_files(self, values):
        self._list_of_files = values

    @property
    def list_of_dirs(self):
        return self._list_of_dirs

    @list_of_dirs.setter
    def list_of_dirs(self, values):
        self._list_of_dirs = values

    @property
    def list_of_dir_files(self):
        return self._list_of_dir_files

    @list_of_dir_files.setter
    def list_of_dir_files(self, values):
        self._list_of_dir_files = values

    @property
    def path_to_dir(self):
        return self._path_to_dir

    @path_to_dir.setter
    def path_to_dir(self, value):
        self._path_to_dir = value

    @property
    def list_of_json_files(self):
        return self._list_of_json_files

    @list_of_json_files.setter
    def list_of_json_files(self, values):
        self._list_of_json_files = values

    @property
    def json_tuples(self):
        return self._json_tuples

    @json_tuples.setter
    def json_tuples(self, values):
        self._json_tuples = values

    def list_directories_and_files(self, path_to_directory):
        self.path_to_dir = path_to_directory
        for (dirpath, dirnames, filenames) in walk(self.path_to_dir):
                for filename in filenames:
                    self.list_of_files.append(filename)
                    self.list_of_dirs.append(dirpath)
                    self.list_of_dir_files.append(path.join(dirpath, filename))

    def dict_to_tuple(self, dictionary):
        json_tuple = [tuple(d.values()) for d in dictionary]
        self._json_tuples = json_tuple
