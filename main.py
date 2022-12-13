import logging
import argparse
import json
from sqlite3_implementer.sqlite3_writer import SqliteWriter
from directory_walker.directory_walker import DirectoryWalker

def argument_parser():
    parser = argparse.ArgumentParser(description="Parser to read a filename from the command.")
    parser.add_argument("-d", "--dir",
                        help="Name of the path containing the json files, without / in the end", required=True)
    parser.add_argument("-m", "--multiple", action="store_true", required=False,
                        help="Add this, if you want to analyze multiple repositories, which are in the given path.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Whether to display logging information.")
    parser.add_argument("-n", "--name",
                        help="Name of the database file to be saved. Default: soccminer_db")
    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    directory_walker = DirectoryWalker()
    directory_walker.list_directories_and_files(path_to_directory=args.dir)

    sq3writer = SqliteWriter()
    sq3writer.initialize_db()

    for file_location in directory_walker.list_of_dir_files:
        with open(file_location, 'r') as f:
            single_json = json.load(f)
            directory_walker.list_of_json_files.extend(single_json)

    # Cleaning up the unnecessasry json-data files, keeping only the ones with the comments.
    directory_walker.list_of_json_files = [x for x in directory_walker.list_of_json_files if isinstance(x, dict)]
    directory_walker.list_of_json_files = [x for x in directory_walker.list_of_json_files if len(x) == 17]
    directory_walker.dict_to_tuple(dictionary=directory_walker.list_of_json_files)

    # Writing the results into a db
    sq3writer.insert_many_json_from_file_to_db(values=directory_walker.json_tuples)



