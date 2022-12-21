import logging
import argparse
import json
import re
from ast import literal_eval
from sqlite3_implementer.sqlite3_writer import SqliteWriter
from directory_walker.directory_walker import DirectoryWalker


def argument_parser():
    parser = argparse.ArgumentParser(description="Parser to read a filename from the command.")
    parser.add_argument("-sd", "--soccdir",
                        help="Name of the path containing the soccminer save location, without / in the end", required=False)
    parser.add_argument("-pd", "--pmddir",
                        help="Name of the path and file containing the json-file from pmd",
                        required=False)
    parser.add_argument("-pp", "--pmdproject",
                        help="Name of the project (directory name) analyzed with pmd",
                        required=False)

    parser.add_argument("-m", "--multiple", action="store_true", required=False,
                        help="Add this, if you want to analyze multiple repositories, which are in the given path.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Whether to display logging information.")
    parser.add_argument("-n", "--name",
                        help="Name of the database file to be saved. Default: soccminer_db")
    parser.add_argument("-a", "--analyzer",
                        default="soccminer",
                        const="soccminer",
                        nargs="?",
                        choices=["soccminer", "pmd"],
                        help="Name of the analyzer used. Can be either 'soccminer' or 'pmd. Default: %(default)s",
                        required=True)
    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    analyzer = args.analyzer

    sq3writer = SqliteWriter()
    sq3writer.initialize_db()

    if analyzer == "soccminer":
        directory_walker = DirectoryWalker()
        directory_walker.list_directories_and_files(path_to_directory=args.soccdir)

        for file_location in directory_walker.list_of_dir_files:
            if "ClassInfo_attributes.json" in file_location:
                with open(file_location, 'r') as f:
                    json_data = json.load(f)
                    for item in json_data:
                        directory_walker.list_of_json_class_files.append(item)
            else:
                with open(file_location, 'r') as f:
                    single_json = json.load(f)
                    if "Comment_Category" in single_json:
                        directory_walker.list_of_json_files.append(single_json)
                    elif "Method_Category" in single_json:
                        directory_walker.list_of_json_method_files.append(single_json)
                    elif "Enum_Signature" in single_json:
                        directory_walker.list_of_json_enum_files.append(single_json)
                    elif "File_Comments_Count" in single_json:
                        directory_walker.list_of_json_file_files.append(single_json)
                    elif "Interface_Signature" in single_json:
                        directory_walker.list_of_json_interface_files.append(single_json)
                    elif "Package_Serialization_File_URL" in single_json:
                        directory_walker.list_of_json_package_files.append(single_json)
                    elif "Static_Block_Source_File" in single_json:
                        directory_walker.list_of_json_staticblock_files.append(single_json)

        # Cleaning up the unnecessasry json-data files, keeping only the ones with the comments.
        directory_walker.list_of_json_files = [x for x in directory_walker.list_of_json_files if isinstance(x, dict)]
        directory_walker.list_of_json_files = [x for x in directory_walker.list_of_json_files if len(x) == 17]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_files, type="comment")
        directory_walker.list_of_json_files = []
        # Writing the results into a db
        sq3writer.insert_many_comments_from_soccminer_to_db(values=directory_walker.json_tuples)

        # Cleaning up classfiles
        directory_walker.list_of_json_class_files = [x for x in directory_walker.list_of_json_class_files if
                                                     isinstance(x, dict)]
        directory_walker.list_of_json_class_files = [x for x in directory_walker.list_of_json_class_files if
                                                     len(x) == 8]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_class_files, type="class")
        directory_walker.list_of_json_class_files = []
        # Writing the results into a db
        sq3writer.insert_many_classes_from_soccminer_to_db(values=directory_walker.json_class_tuples)

        # Cleaning up methodfiles
        directory_walker.list_of_json_method_files = [x for x in directory_walker.list_of_json_method_files if isinstance(x, dict)]
        directory_walker.list_of_json_method_files = [x for x in directory_walker.list_of_json_method_files if len(x) == 9]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_method_files, type="method")
        directory_walker.list_of_json_method_files = []
        # Writing the results into a db
        sq3writer.insert_many_methods_from_soccminer_to_db(values=directory_walker.json_method_tuples)

        # Cleaning up enumfiles
        directory_walker.list_of_json_enum_files = [x for x in directory_walker.list_of_json_enum_files if isinstance(x, dict)]
        directory_walker.list_of_json_enum_files = [x for x in directory_walker.list_of_json_enum_files if len(x) == 6]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_enum_files, type="enum")
        directory_walker.list_of_json_enum_files = []
        # Writing the results into a db
        sq3writer.insert_many_enums_from_soccminer_to_db(values=directory_walker.json_enum_tuples)

        # Cleaning up filefiles
        directory_walker.list_of_json_file_files = [x for x in directory_walker.list_of_json_file_files if isinstance(x, dict)]
        directory_walker.list_of_json_file_files = [x for x in directory_walker.list_of_json_file_files if len(x) == 3]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_file_files, type="file")
        directory_walker.list_of_json_file_files = []
        # Writing the results into a db
        sq3writer.insert_many_files_from_soccminer_to_db(values=directory_walker.json_file_tuples)

        # Cleaning up interfacefiles
        directory_walker.list_of_json_interface_files = [x for x in directory_walker.list_of_json_interface_files if isinstance(x, dict)]
        directory_walker.list_of_json_interface_files = [x for x in directory_walker.list_of_json_interface_files if len(x) == 6]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_interface_files, type="interface")
        directory_walker.list_of_json_interface_files = []
        # Writing the results into a db
        sq3writer.insert_many_interfaces_from_soccminer_to_db(values=directory_walker.json_interface_tuples)

        # Cleaning up packagefiles
        directory_walker.list_of_json_package_files = [x for x in directory_walker.list_of_json_package_files if isinstance(x, dict)]
        directory_walker.list_of_json_package_files = [x for x in directory_walker.list_of_json_package_files if len(x) == 5]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_package_files, type="package")
        directory_walker.list_of_json_package_files = []
        # Writing the results into a db
        sq3writer.insert_many_packages_from_soccminer_to_db(values=directory_walker.json_package_tuples)

        # Cleaning up staticblockfiles
        directory_walker.list_of_json_staticblock_files = [x for x in directory_walker.list_of_json_staticblock_files if isinstance(x, dict)]
        directory_walker.list_of_json_staticblock_files = [x for x in directory_walker.list_of_json_staticblock_files if len(x) == 3]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_staticblock_files, type="staticblock")
        directory_walker.list_of_json_staticblock_files = []
        # Writing the results into a db
        sq3writer.insert_many_staticblocks_from_soccminer_to_db(values=directory_walker.json_staticblock_tuples)


    elif analyzer == "pmd":
        with open(args.pmddir, 'r') as f:
            single_json = json.load(f)
        pmd_list_of_files = single_json["files"]
        project_name = args.pmdproject
        # Change the filenames to match the style in soccminer
        tuple_list_of_pmd_info = []
        logging.info("Starting to read PMD files")
        for individual_file in pmd_list_of_files:
            individual_file["filename"] = re.sub(".*" + project_name + "\\\\", "", individual_file["filename"])
            #individual_file["filename"] = re.sub(".*argouml-VERSION_0_34\\\\", "", individual_file["filename"])
            individual_file["filename"] = re.sub("\\\\", ".", individual_file["filename"])
            for violation in individual_file["violations"]:
                #individual_list_entry.append((individual_file["filename"], *list(violation.items())))
                tuple_list_of_pmd_info.append((project_name,
                                               individual_file["filename"],
                                               violation["beginline"],
                                               violation["begincolumn"],
                                               violation["endline"],
                                               violation["endcolumn"],
                                               violation["description"],
                                               violation["rule"],
                                               violation["ruleset"],
                                               violation["priority"],
                                               violation["externalInfoUrl"]))
        logging.info("PMD files read into a list of tuples.")

        sq3writer.insert_many_json_from_pmd_to_db(tuple_list_of_pmd_info)


    else:
        logging.info("Analyzer needs to be either 'soccminer' or 'pmd'.")

