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
        cur.execute("CREATE TABLE if NOT EXISTS comment(comment_key integer PRIMARY KEY AUTOINCREMENT,"
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

        cur.execute("CREATE TABLE if NOT EXISTS method(method_key integer PRIMARY KEY AUTOINCREMENT,"
                    "Method_Category text,"
                    "Method_LOC int,"
                    "Method_Line_No int,"
                    "Method_Name text,"
                    "Method_Param_Count int,"
                    "Method_Signature text,"
                    "Method_Source_File text,"
                    "Method_Specifier text,"
                    "Method_Type text)")
        self._connection.commit()

        cur.execute("CREATE TABLE if NOT EXISTS class(class_key integer PRIMARY KEY AUTOINCREMENT,"
                    "Class_LOC int,"
                    "Class_Line_No int,"
                    "Class_Name text,"
                    "Class_Nested_Level int,"
                    "Class_Signature text,"
                    "Class_Source_File text,"
                    "Class_Specifier text,"
                    "Class_Type text)")
        self._connection.commit()

        cur.execute("CREATE TABLE if NOT EXISTS enum(enum_key integer PRIMARY KEY AUTOINCREMENT,"
                    "Enum_LOC int,"
                    "Enum_Line_No int,"
                    "Enum_Name text,"
                    "Enum_Signature text,"
                    "Enum_Source_File text,"
                    "Enum_Specifier text)")
        self._connection.commit()

        cur.execute("CREATE TABLE if NOT EXISTS file(file_key integer PRIMARY KEY AUTOINCREMENT,"
                    "File_Comments_Count int,"
                    "File_LOC int,"
                    "Source_File text)")
        self._connection.commit()

        cur.execute("CREATE TABLE if NOT EXISTS interface(interface_key integer PRIMARY KEY AUTOINCREMENT,"
                    "Interface_LOC int,"
                    "Interface_Line_No int,"
                    "Interface_Name text,"
                    "Interface_Signature text,"
                    "Interface_Source_File text,"
                    "Interface_Specifier text)")
        self._connection.commit()

        cur.execute("CREATE TABLE if NOT EXISTS package(package_key integer PRIMARY KEY AUTOINCREMENT,"
                    "Package_LOC int,"
                    "Package_Line_No int,"
                    "Package_Name text,"
                    "Package_Serialization_File_URL text,"
                    "Package_Source_File text)")
        self._connection.commit()

        cur.execute("CREATE TABLE if NOT EXISTS staticblock(staticblock_key integer PRIMARY KEY AUTOINCREMENT,"
                    "Static_Block_LOC int,"
                    "Static_Block_Line_No int,"
                    "Static_Block_Source_File text)")
        self._connection.commit()


        cur.execute("CREATE TABLE if NOT EXISTS pmd(pmd_key integer PRIMARY KEY AUTOINCREMENT,"
                    "Filename text,"
                    "Begin_Line int,"
                    "Begin_Column int,"
                    "End_Line int,"
                    "End_Column int,"
                    "Description text,"
                    "Rule text,"
                    "Rule_Set text,"
                    "Priority integer,"
                    "External_Info_Url text)")
        self._connection.commit()
        self.close_connection()

    def insert_single_comment_from_soccminer_to_db(self, datafile=None):
        logging.info("Reading a json to dictionary %s", datafile)
        cur = self.connect_to_db().cursor()
        cur.execute('INSERT INTO comment (Comment_Assoc_Block_Node,'
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

    def insert_many_comments_from_soccminer_to_db(self, values):
        logging.info("Writing many comments to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany(
                "INSERT into comment(Comment_Assoc_Block_Node,"
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

    def insert_many_methods_from_soccminer_to_db(self, values):
        logging.info("Writing many methods to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany(
                "INSERT into method(Method_Category,"
                "Method_LOC,"
                "Method_Line_No,"
                "Method_Name,"
                "Method_Param_Count,"
                "Method_Signature,"
                "Method_Source_File,"
                "Method_Specifier,"
                "Method_Type) VALUES (?,?,?,?,?,?,?,?,?)",
                values)
            self._connection.commit()
        except Exception as e:
            print(e)
        self.close_connection()

    def insert_many_enums_from_soccminer_to_db(self, values):
        logging.info("Writing many enums to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany(
                "INSERT into enum(Enum_LOC,"
                "Enum_Line_No,"
                "Enum_Name,"
                "Enum_Signature,"
                "Enum_Source_File,"
                "Enum_Specifier) VALUES (?,?,?,?,?,?)",
                values)
            self._connection.commit()
        except Exception as e:
            print(e)
        self.close_connection()

    def insert_many_files_from_soccminer_to_db(self, values):
        logging.info("Writing many files to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany(
                "INSERT into enum(File_Comments_Count,"
                "File_LOC,"
                "Source_File) VALUES (?,?,?)",
                values)
            self._connection.commit()
        except Exception as e:
            print(e)
        self.close_connection()
    def insert_many_classes_from_soccminer_to_db(self, values):
        logging.info("Writing many classes to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany("INSERT into class(Class_LOC,"
                            "Class_Line_No,"
                            "Class_Name,"
                            "Class_Nested_Level,"
                            "Class_Signature,"
                            "Class_Source_File,"
                            "Class_Specifier,"
                            "Class_Type) VALUES (?,?,?,?,?,?,?,?)""", values)
            self._connection.commit()
        except Exception as e:
            print(e)
        self.close_connection()

    def insert_many_interfaces_from_soccminer_to_db(self, values):
        logging.info("Writing many interfaces to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany(
                "INSERT into interface(Interface_LOC,"
                "Interface_Line_No,"
                "Interface_Name,"
                "Interface_Signature,"
                "Interface_Source_File,"
                "Interface_Specifier) VALUES (?,?,?,?,?,?)",
                values)
            self._connection.commit()
        except Exception as e:
            print(e)
        self.close_connection()

    def insert_many_packages_from_soccminer_to_db(self, values):
        logging.info("Writing many packages to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany("INSERT into package(Package_LOC,"
                            "Package_Line_No,"
                            "Package_Name,"
                            "Package_Serialization_File_URL,"
                            "Package_Source_File) VALUES (?,?,?,?,?)""", values)
            self._connection.commit()
        except Exception as e:
            print(e)
        self.close_connection()

    def insert_many_staticblocks_from_soccminer_to_db(self, values):
        logging.info("Writing many staticblocks to db %s", (self._db_name,))
        cur = self.connect_to_db().cursor()
        # cur.executemany("INSERT into comments VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        try:
            cur.executemany("INSERT into package(Static_Block_LOC,"
                            "Static_Block_Line_No,"
                            "Static_Block_Source_File) VALUES (?,?,?)""", values)
            self._connection.commit()
        except Exception as e:
            print(e)
        self.close_connection()

    def insert_many_json_from_pmd_to_db(self, values):
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


