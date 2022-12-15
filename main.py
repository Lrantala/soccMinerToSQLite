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

    if analyzer == "soccminer":
        directory_walker = DirectoryWalker()
        directory_walker.list_directories_and_files(path_to_directory=args.soccdir)

        sq3writer = SqliteWriter()
        sq3writer.initialize_db()

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
                    #elif "Class_Signature" in single_json:
                    #    directory_walker.list_of_json_class_files.append(single_json)

        # Cleaning up classfiles
        directory_walker.list_of_json_class_files = [x for x in directory_walker.list_of_json_class_files if
                                                     isinstance(x, dict)]
        directory_walker.list_of_json_class_files = [x for x in directory_walker.list_of_json_class_files if
                                                     len(x) == 8]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_class_files, type="class")
        directory_walker.list_of_json_class_files = []
        # Writing the results into a db
        sq3writer.insert_many_classes_from_soccminer_to_db(values=directory_walker.json_class_tuples)

        # Cleaning up the unnecessasry json-data files, keeping only the ones with the comments.
        directory_walker.list_of_json_files = [x for x in directory_walker.list_of_json_files if isinstance(x, dict)]
        directory_walker.list_of_json_files = [x for x in directory_walker.list_of_json_files if len(x) == 17]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_files, type="comment")
        directory_walker.list_of_json_files = []
        # Writing the results into a db
        sq3writer.insert_many_comments_from_soccminer_to_db(values=directory_walker.json_tuples)

        # Cleaning up methodfiles
        directory_walker.list_of_json_method_files = [x for x in directory_walker.list_of_json_method_files if isinstance(x, dict)]
        directory_walker.list_of_json_method_files = [x for x in directory_walker.list_of_json_method_files if len(x) == 9]
        directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_method_files, type="method")
        directory_walker.list_of_json_method_files = []
        # Writing the results into a db
        sq3writer.insert_many_methods_from_soccminer_to_db(values=directory_walker.json_method_tuples)

    elif analyzer == "pmd":
        with open(args.pmddir, 'r') as f:
            single_json = json.load(f)
        pmd_list_of_files = single_json["files"]
        # Change the filenames to match the style in soccminer
        for individual_file in pmd_list_of_files:
            print(individual_file["filename"])
            individual_file["filename"] = re.sub(".*argouml-VERSION_0_34\\\\", "", individual_file["filename"])
            individual_file["filename"] = re.sub("\\\\", ".", individual_file["filename"])
    else:
        logging.info("Analyzer needs to be either 'soccminer' or 'pmd'.")

