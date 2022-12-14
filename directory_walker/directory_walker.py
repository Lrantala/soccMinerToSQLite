from os import walk
from os import path


class DirectoryWalker:

    def __init__(self):
        self._list_of_json_interface_files = []
        self._list_of_files = []
        self._list_of_dirs = []
        self._list_of_dir_files = []
        self._path_to_dir = ""
        self._list_of_json_files = []
        self._list_of_json_method_files = []
        self._json_tuples = []
        self._json_method_tuples = []
        self._list_of_json_class_files = []
        self._json_class_tuples = []
        self._list_of_json_enum_files = []
        self._json_enum_tuples = []
        self._list_of_json_file_files = []
        self._json_file_tuples = []
        self._list_of_json_interface_files = []
        self._json_interface_tuples = []
        self._list_of_json_package_files = []
        self._json_package_tuples = []
        self._list_of_json_staticblock_files = []
        self._json_staticblock_tuples = []

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
    def list_of_json_method_files(self):
        return self._list_of_json_method_files

    @list_of_json_method_files.setter
    def list_of_json_method_files(self, values):
        self._list_of_json_method_files = values

    @property
    def json_method_tuples(self):
        return self._json_method_tuples

    @json_method_tuples.setter
    def json_method_tuples(self, values):
        self._json_method_tuples = values

    @property
    def list_of_json_class_files(self):
        return self._list_of_json_class_files

    @list_of_json_class_files.setter
    def list_of_json_class_files(self, values):
        self._list_of_json_class_files = values

    @property
    def json_class_tuples(self):
        return self._json_class_tuples

    @json_class_tuples.setter
    def json_class_tuples(self, values):
        self._json_class_tuples = values

    @property
    def list_of_json_enum_files(self):
        return self._list_of_json_enum_files

    @list_of_json_enum_files.setter
    def list_of_json_enum_files(self, values):
        self._list_of_json_enum_files = values

    @property
    def json_enum_tuples(self):
        return self._json_enum_tuples

    @json_enum_tuples.setter
    def json_enum_tuples(self, values):
        self._json_enum_tuples = values

    @property
    def list_of_json_file_files(self):
        return self._list_of_json_file_files

    @list_of_json_file_files.setter
    def list_of_json_file_files(self, values):
        self._list_of_json_file_files = values

    @property
    def json_file_tuples(self):
        return self._json_file_tuples

    @json_file_tuples.setter
    def json_file_tuples(self, values):
        self._json_file_tuples = values

    @property
    def list_of_json_interface_files(self):
        return self._list_of_json_interface_files

    @list_of_json_interface_files.setter
    def list_of_json_interface_files(self, values):
        self._list_of_json_interface_files = values

    @property
    def json_interface_tuples(self):
        return self._json_interface_tuples

    @json_interface_tuples.setter
    def json_interface_tuples(self, values):
        self._json_interface_tuples = values

    @property
    def list_of_json_package_files(self):
        return self._list_of_json_package_files

    @list_of_json_package_files.setter
    def list_of_json_package_files(self, values):
        self._list_of_json_package_files = values

    @property
    def json_package_tuples(self):
        return self._json_package_tuples

    @json_package_tuples.setter
    def json_package_tuples(self, values):
        self._json_package_tuples = values

    @property
    def list_of_json_staticblock_files(self):
        return self._list_of_json_staticblock_files

    @list_of_json_staticblock_files.setter
    def list_of_json_staticblock_files(self, values):
        self._list_of_json_staticblock_files = values

    @property
    def json_staticblock_tuples(self):
        return self._json_staticblock_tuples

    @json_staticblock_tuples.setter
    def json_staticblock_tuples(self, values):
        self._json_staticblock_tuples = values

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

    def dict_to_tuple(self, dictionary, type):
        json_tuple = [tuple(d.values()) for d in dictionary]
        if type == "comment":
            self._json_tuples = json_tuple
        elif type == "method":
            self._json_method_tuples = json_tuple
        elif type == "class":
            self._json_class_tuples = json_tuple
        elif type == "enum":
            self._json_enum_tuples = json_tuple
        elif type == "file":
            self._json_file_tuples = json_tuple
        elif type == "interface":
            self._json_interface_tuples = json_tuple
        elif type == "package":
            self._json_package_tuples = json_tuple
        elif type == "staticblock":
            self._json_staticblock_tuples = json_tuple
