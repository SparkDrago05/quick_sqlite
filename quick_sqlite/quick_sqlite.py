import sqlite3
import os
from cryptography.fernet import Fernet
from .column import Column


class QuickSqlite():
    """Class to use SQLite3.

    Args:
        db_path (str): The path to the database.
        protect (bool): If True, the database will be encrypted.
        key (str): The Fernet key to use for encryption.
    """

    def __init__(self, db_path: str, protect: bool, key: str = ""):
        """Initializes the QuickSqlite Class.

        Args:
            db_path (str): The path to the database.
            protect (bool): If True, the database will be encrypted.
            key (str): The Fernet key to use for encryption.
        """
        self.__db_path = db_path
        self.__protect = protect
        self.__database_encrypted = True
        self.__key = key
        if protect is None and key == '':
            raise ValueError(
                "If Protect is True, you must provide a valid Fernet key.")

    def __connect(self):
        global conn, cursor
        if self.__protect == False:
            conn = sqlite3.connect(self.__db_path)
            cursor = conn.cursor()
        elif self.__protect == True:
            if os.path.exists(self.__db_path) == False:
                self.__database_encrypted = False
            if self.__database_encrypted == False:
                conn = sqlite3.connect(self.__db_path)
                cursor = conn.cursor()
                self._encrypt_database(self.__db_path, self.__key)
                self.__database_encrypted = True
            if self.__database_encrypted:

                self._decrypt_database(self.__db_path, self.__key)
                conn = sqlite3.connect(self.__db_path)
                cursor = conn.cursor()
                self.__database_encrypted = False

    def __close(self):
        if self.__protect == False:
            cursor.close()
            conn.close()
        elif self.__protect == True:
            if self.__database_encrypted == False:
                self._encrypt_database(self.__db_path, self.__key)
                self.__database_encrypted = True

    def _encrypt_database(self, filename, key):
        """
        Given a filename (str) and key (bytes), it encrypts the file and write it
        """
        f = Fernet(key)
        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()
            # encrypt data
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)

    def _decrypt_database(self, filename, key):
        """
        Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        f = Fernet(key)
        with open(filename, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
        decrypted_data = f.decrypt(encrypted_data)
        # write the original file
        with open(filename, "wb") as file:
            file.write(decrypted_data)

    def create_table(self, table_name: str, columns: list[Column]):
        """Creates the table with specified name and column name(s).

        Args:
            table_name (str): The name of the table to create.
            columns (list[Column]): Column class using quick_sqlite.Column() class.
        """
        create_table_query = 'CREATE TABLE IF NOT EXISTS {name} ({columns});'.format(
            name=table_name, columns=', '.join(str(column) for column in columns))

        self.__connect()
        cursor.execute(create_table_query)
        self.__close()

    def rename_table(self, old_table_name: str, new_table_name: str):
        """Renames the specified table.

        Args:
            table_name (str): The name of the table to rename.
            old_table_name (str): The old name of the table.
            new_table_name (str): The new name of the table.
        """
        table_exists = self.check_table_exists(old_table_name)
        self.__connect()
        if table_exists:
            cursor.execute(
                f"ALTER TABLE {old_table_name} RENAME TO {new_table_name}")
        self.__close()

    def check_table_exists(self, table_name: str) -> bool:
        """Checks if specified table exists in the database.

        Args:
            table_name (str): Name of the table to check.

        Returns:
            bool: True if table exists, False otherwise.
        """
        self.__connect()
        cursor.execute(
            f"SELECT name from sqlite_master WHERE type = 'table' AND name = '{table_name}'")
        table = cursor.fetchone()
        self.__close()
        if table:
            return True
        elif table is None:
            return False

    def delete_table(self, table_name: str):
        """Deletes the specified table.

        Args:
            table_name (str): The name of the table to delete.
        """
        self.__connect()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.__close()

    def insert_data(self, table_name: str, data: dict):
        """Inserts the data in the specified column of the specified table.

        Args:
            table_name (str): The name of the table in which data is to be inserted.
            data (dict): The data dictionary with key as column_name and value as column_value i.e. data 
        """
        insert_table_query = "INSERT INTO '{table_name}' ('{x}') VALUES ('{y}')".format(
            table_name=table_name, x="', '".join(v for v in data.keys()), y="', '".join(v for v in data.values()))

        self.__connect()
        cursor.execute(insert_table_query)
        conn.commit()
        self.__close()

    def update_data(self, table_name: str, data: dict, filter_column_name: str, filter_column_data: str):
        """Updates the data in the specified column of specified table.

        Args:
            table_name (str): The name of the table in which data is to be updated.
            column_name (str): The name of the column in which data is to be updated.
            data (dict): The data dictionary with key as column_name and value as column_value i.e. data 
            filter_column_name (str): The name of a column to filter the row.
            filter_column_data (str): The data of a column to filter the row.
        """
        update_query = "UPDATE {table_name} SET {values} WHERE {filter_column_name} = '{filter_column_data}'".\
            format(table_name=table_name, values=', '.join([' = '.join(
                [field_name, '?'])for field_name in data]), filter_column_name=filter_column_name, filter_column_data=filter_column_data)

        self.__connect()
        cursor.execute(update_query, tuple(data.values()))
        conn.commit()
        self.__close()

    def fetch_table(self, table_name: str, row_limit: int = None) -> list[tuple]:
        """Returns all data of the specified table.

        Args:
            table_name (str): The name of the table of which you want the data.
            row_limit (int): The number of rows to fetch.

        Returns:
            list[tuple]: Returns the list containing data of each row in tuples.
        """
        self.__connect()
        cursor.execute(f"SELECT * FROM {table_name}")
        if row_limit is None:
            result = cursor.fetchall()
        elif row_limit is not None:
            result = cursor.fetchmany(row_limit)
        self.__close()
        return result

    def add_column(self, table_name: str, column: Column):
        """Adds a column to the specified table.

        Args:
            table_name (str): The name of the table to add the column to.
            column (Column): The column to add. You should use quick_sqlite.Column() class.
        """
        add_column_query = f"ALTER TABLE {table_name} ADD {str(column)}"
        self.__connect()
        query = cursor.execute(
            f"SELECT COUNT(*) AS CNTREC FROM pragma_table_info('{table_name}') WHERE name='{column.name}'")
        column_exist = query.fetchone()
        column_exist = column_exist[0] > 0
        if not column_exist:
            cursor.execute(add_column_query)
        self.__close()

    def rename_column(self, table_name: str, old_column_name: str, new_column_name: str):
        """Renames a column in the specified table.

        Args:
            table_name (str): The name of the table to rename the column in.
            old_column_name (str): The name of the column to rename.
            new_column_name (str): The new name of the column.
        """
        self.__connect()
        query = cursor.execute(
            f"SELECT COUNT(*) AS CNTREC FROM pragma_table_info('{table_name}') WHERE name='{old_column_name}'")
        column_exist = query.fetchone()
        column_exist = column_exist[0] > 0
        if column_exist:
            cursor.execute(
                f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}")
        self.__close()

    def delete_column(self, table_name: str, column_name: str):
        """Deletes a column from the specified table.

        Args:
            table_name (str): The name of the table to delete the column from.
            column_name (str): The name of the column to delete.
        """
        self.__connect()
        query = cursor.execute(
            f"SELECT COUNT(*) AS CNTREC FROM pragma_table_info('{table_name}') WHERE name='{column_name}'")
        column_exist = query.fetchone()
        column_exist = column_exist[0] > 0
        if column_exist:
            cursor.execute(
                f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
        self.__close()

    def fetch_column(self, table_name: str, column_name: str) -> list[tuple]:
        """Returns a specified column of the specified table.

        Args:
            table_name (str): The name of the table of which you want column.
            column_name (str): The name of the column of which you want data.

        Returns:
            list[tuple]: Returns the list containing data of each row in tuples.
        """
        self.__connect()
        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        result = cursor.fetchall()
        self.__close()
        return result

    def check_column_exists(self, table_name, column_name) -> bool:
        """Checks if specified column exists in the specified table.

        Args:
            table_name (str): Name of the table to check.
            column_name (str): The name of the column to check.

        Returns:
            bool: True if column exists, False otherwise.
        """
        self.__connect()

        cursor.execute(
            f"SELECT COUNT(*) AS CNTREC FROM pragma_table_info('{table_name}') WHERE name='{column_name}'")
        column = cursor.fetchone()
        column_exist = column[0] > 0

        if column_exist:
            return True
        elif not column_exist:
            return False

        self.__close()

    def fetch_data(self, table_name: str, column_name: str, filter_column_name: str, filter_column_data: str, condition: str) -> tuple[str]:
        """Returns a specified data from a specified column.

        Args:
            table_name (str): The name of the table of which you want the data.
            column_name (str): The name of the column of which you want the data.
            filter_column_name (str): The name of the column you want to be filtered through.
            filter_column_data (str): The data of the column you want to be filtered through.
            condition: Condition to search the data. Available are: =, <, >, <=, >=, <>(not equal).
                this will look like: {filter_column_name} {condition} {filter_column_data}

        Returns:
            tuple[str]: Returns a tuple consisting of the data of the specified column as string.
        """
        self.__connect()
        """
        filter_column_name_array = filter_column_name.split()
        edited_array = []
        for filter_column_name_value in filter_column_name_array:
            edited_array.append(filter_column_name_value + '=?')

        edited_string = ' and '.join(edited_array).replace(',', '')
        filter_data_tuple = tuple(filter_column_data)
        """

        #cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE {edited_string}", (filter_data_tuple))
        cursor.execute(
            f"SELECT {column_name} FROM {table_name} WHERE {filter_column_name} {condition} {filter_column_data}")
        result = cursor.fetchone()
        self.__close()
        return result

    def delete_row(self, table_name: str, column_name: str, data: str):
        """Deletes the specified row from the table.

        Args:
            table_name (str): The name of the table of which you want to delete the data.
            column_name (str): The name of the column of which you want to delete the data.
            data (str): The data of the row to be deleted.
        """
        self.__connect()
        cursor.execute(
            f"DELETE FROM {table_name} WHERE {column_name} = ?", (data,))
        conn.commit()
        self.__close()
