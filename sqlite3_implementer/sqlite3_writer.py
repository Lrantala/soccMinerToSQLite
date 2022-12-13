import logging
import sqlite3


class SqliteWriter():
    def __init__(self):
        self._db_name = "./save/soccminer.db"
        self._connection = None

    def connect_to_db(self):
        logging.info("Initializing connection to db.")
        self._connection = sqlite3.connect(self._db_name)
        connection_name = (self._db_name,)
        logging.info("Connection created to db %s", connection_name)
        return self._connection

    def close_connection(self):
        self._connection.close()

    def initialize_db(self):
        logging.info("Initializing db.")
        cur = self.connect_to_db().cursor()
        # Check if the table exists before creating it
        cur.execute("CREATE TABLE if NOT EXISTS comments(comment_key integer PRIMARY KEY AUTOINCREMENT,"
                    "Comment_Assoc_Block_Node text,"
                    "Comment_Category text,"
                    "Comment_Content text,"
                    "Comment_First_Element_In text,"
                    "Comment_Immediate_Preceding_Code text,"
                    "Comment_Immediate_Succeeding_Code text,"
                    "Comment_Last_Element_In text,"
                    "Comment_Level text,"
                    "Comment_Line_No integer,"
                    "Comment_Parent_Identifier text,"
                    "Comment_Parent_Trace text,"
                    "Comment_Preceding_Node text,"
                    "Comment_Source_File text,"
                    "Comment_SubCategory text,"
                    "Comment_SubCatg_Type text,"
                    "Comment_Succeeding_Node text,"
                    "Comment_Type text)")
        self._connection.commit()
        self.close_connection()

    def insert_json_from_file_to_db(self, datafile=None):
        logging.info("Reading a json to dictionary %s", datafile)
        cur = self.connect_to_db().cursor()
        cur.execute('INSERT INTO comments (Comment_Assoc_Block_Node,'
                        'Comment_Category,'
                        'Comment_Content,'
                        'Comment_First_Element_In,'
                        'Comment_Immediate_Preceding_Code,'
                        'Comment_Immediate_Succeeding_Code,'
                        'Comment_Last_Element_In,'
                        'Comment_Level,'
                        'Comment_Line_No,'
                        'Comment_Parent_Identifier,'
                        'Comment_Parent_Trace,'
                        'Comment_Preceding_Node,'
                        'Comment_Source_File,'
                        'Comment_SubCategory,'
                        'Comment_SubCatg_Type,'
                        'Comment_Succeeding_Node,'
                        'Comment_Type) '
                         'VALUES (:Comment_Assoc_Block_Node,'
                        ':Comment_Category,'
                        ':Comment_Content,'
                        ':Comment_First_Element_In,'
                        ':Comment_Immediate_Preceding_Code,'
                        ':Comment_Immediate_Succeeding_Code,'
                        ':Comment_Last_Element_In,'
                        ':Comment_Level,'
                        ':Comment_Line_No,'
                        ':Comment_Parent_Identifier,'
                        ':Comment_Parent_Trace,'
                        ':Comment_Preceding_Node,'
                        ':Comment_Source_File,'
                        ':Comment_SubCategory,'
                        ':Comment_SubCatg_Type,'
                        ':Comment_Succeeding_Node,'
                        ':Comment_Type)', datafile)
        self._connection.commit()
        self.close_connection()

    def insert_many_json_from_file_to_db(self, values):
        logging.info("Writing many comments to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany(
                "INSERT into comments(Comment_Assoc_Block_Node,"
                "Comment_Category,"
                "Comment_Content,"
                "Comment_First_Element_In,"
                "Comment_Immediate_Preceding_Code,"
                "Comment_Immediate_Succeeding_Code,"
                "Comment_Last_Element_In,"
                "Comment_Level,"
                "Comment_Line_No,"
                "Comment_Parent_Identifier,"
                "Comment_Parent_Trace,"
                "Comment_Preceding_Node,"
                "Comment_Source_File,"
                "Comment_SubCategory,"
                "Comment_SubCatg_Type,"
                "Comment_Succeeding_Node,"
                "Comment_Type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                values)
            self._connection.commit()
        except Exception as e:
            print(e)
        self.close_connection()
