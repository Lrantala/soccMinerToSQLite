# soccMinerToSQLite

This program saves the JSON-data mined with Soccminer-tool (https://github.com/M3SOulu/soccminer) to a SQLite database.

Currently accepts Soccminer data mined at "all"-level, and saves this comment data to a SQLite database.
Also accepts PMD data saved in json-format and saves it to a SQLite database.

In order to connent Soccminer and PMD, the names of the projects must match when importing them. Soccminer project name is taken as the directory name of the project without the path to it. For PMD, the name of the project must be given.

<h3>Parameters</h3>

Currently, only the following parameters are used:

- -sd (--soccdir): The directory containing the mined data directories, without the / in the end. E.g., ..\..\soccminer\save\SoCCMiner_Mined_Entities\NAME_OF_THE_REPOSITORY_DIRECTORY

- -pd (--pmddir): Name of the path and file containing the json-file from pmd. E.g., ..\save\pmd_json\PMD_PROJECT_V2.json
- -pp (--pmdproject): Name of the project (directory name) analyzed with pmd. E.g., PMD_PROJECT_V2
- -a (--analyzer): Analyzer used. Must be either soccminer or pmd
- -v (--verbose): A boolean flag whether to display logging information or not.

