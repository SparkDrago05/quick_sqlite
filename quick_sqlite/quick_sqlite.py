import sqlite3


class QuickSqlite():
    """Class to use sqlite3."""

    def __init__(self, db_name: str):
        self.db_name = db_name

    def connect(self):
        global conn, cursor
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

    def close(self):
        cursor.close()
        conn.close()

    def create_table(self, table_name: str, column_name: str):
        """
        Creates the table with specified name and column name.

        Args:
             table_name (str): The name of the table to create.
             column_name (str): The column(s) name of the table.
        """
        self.connect()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({column_name})")
        self.close()

    def check_table_exists(self, table_name: str, column_name: str) -> bool:
        """
        Checks if specified table exists in the database.

        Args:
             table_name (str): name of the table to check.
             column_name (str): The name of any column of the table.
        """
        self.connect()
        cursor.execute(
            f"SELECT {column_name} from sqlite_master WHERE type = 'table' AND name = '{table_name}'")
        table = cursor.fetchone()
        if table:
            return True
        elif table is None:
            return False
        self.close()

    def delete_table(self, table_name: str):
        """
        Deletes the specified table.

        Args:
             table_name (str): The name of the table to delete.
        """
        self.connect()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.close()

    def alter_table(self, table_name: str, column_function: str, data: str):
        """
        Alters the specified thing of the specified table.

        Args:
             table_name (str): The name of the table to alter.
             column: The column you want to alter.
             data: The data of the thing you want to alter.
        """
        self.connect()
        cursor.execute(
            f"ALTER TABLE {table_name} {column_function} COLUMN {data}")
        self.close()

    def insert_table(self, table_name: str, column_name: str, data: list[str]):
        """
        Inserts the data in the specified column of the specified table.

        Args:
             table_name (str): The name of the table in which data is to be inserted.
             column_name (str): The name of the column in which data is to be inserted.
             data (list[str]): The data to be inserted.
        """
        data_count = len(data)
        loop_count = 0
        question_marks = ''
        data_tuple = tuple(data)
        for i in data:
            loop_count += 1
            question_marks += '?'
            question_marks += ' '
            if not loop_count == data_count:
                question_marks += ','

        self.connect()
        cursor.execute(
            f"INSERT INTO {table_name} ({column_name}) VALUES ({question_marks})", (data_tuple))
        conn.commit()
        self.close()

    def update_table(self, table_name: str, column_name: str, new_data: str, filter_column_name: str, filter_column_data: str):
        """
        Updates the data in the specified column of specified table.

        Args:
             table_name (str): The name of the table in which data is to be updated.
             column_name (str): The name of the column in which data is to be updated.
             data (str): The data to be updated.
             filter_column_name (str): The name of a column to filter the row
             filter_column_data (str): The data of a column to filter the row.
        """
        self.connect()
        cursor.execute(
            f"UPDATE {table_name} SET {column_name} = ? WHERE {filter_column_name} = ?", (new_data, filter_column_data))
        conn.commit()
        self.close()

    def select_table(self, table_name: str) -> list[tuple]:
        """
        Returns all data of the specified table.

        Args:
             table_name: The name of the table of which you want the data.
        """
        self.connect()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        self.close()
        return result

    def select_column(self, table_name: str, column_name: str) -> list[tuple]:
        """
        Returns a specified column of the specified table.

        Args:
             table_name: The name of the table of which you want column.
             column_name: The name of the column of which you want data.
        """
        self.connect()
        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        result = cursor.fetchall()
        self.close()
        return result

    def select_data(self, table_name: str, column_name: str, filter_column_name: str, filter_column_data: str):
        """
        Returns a specified data from a specified column.

        Args:
             table_name (str): The name of the table of which you want the data.
             column_name (str): The name of the column of which you want the data.
             filter_column_name (str): The name of the column you want to be filtered through.
             filter_column_data (str): The data of the column you want to be filtered through.
        """
        self.connect()
        cursor.execute(
            f"SELECT {column_name} FROM {table_name} WHERE {filter_column_name} = ?", (filter_column_data))
        result = cursor.fetchone()
        self.close()
        return result

    def delete_data(self, table_name: str, column_name: str, data: str):
        """
        Deletes the specified row from the table.

        Args:
             table_name (str): The name of the table of which you want to delete the data.
             column_name (str): The name of the column of which you want to delete the data.
             column_data (str): The data of the row to be deleted.
        """
        self.connect()
        cursor.execute(
            f"DELETE FROM {table_name} WHERE {column_name} = ?", (data))
        conn.commit()
        self.close()