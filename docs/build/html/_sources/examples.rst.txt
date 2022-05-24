.. _examples:

Examples
========

Here are examples of how to use the QuickSqlite module.



Creating a database
-------------------

Here's how you can create a single simple database.

.. code-block:: python

    from quick_sqlite import QuickSqlite

    # Create a new database
    db = QuickSqlite('my_database.db', False)

You can also work with multiple databases.

.. code-block:: python

    from quick_sqlite import QuickSqlite

    # Create a simple database
    db = QuickSqlite('my_database.db', False)

    key = b'3kVCk6cXQqLX3HTFMg4XUvHVt7sG__-C25p4uAZvrIE='
    # Create an encrypted database
    db2 = QuickSqlite('my_database2.db', True, key)

You can generate a fernet key using **cryptography** module.

>>> from cryptography.fernet import Fernet
>>> key = Fernet.generate_key()
b'3kVCk6cXQqLX3HTFMg4XUvHVt7sG__-C25p4uAZvrIE='

You can read more about Fernet |location_link|.

.. |location_link| raw:: html

   <a href="https://cryptography.io/en/latest/fernet/" target="_blank">here</a>

Creating a table
----------------

>>> db.create_table('accounts', 'id INT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255)')

Here table name is 'accounts' and columns are 'id', 'name', 'email' and 'password'.
INT and VARCHAR are data types of columns.

Checking for a table
--------------------

>>> db.check_table_exists('accounts', 'password')
True

It returns True as we just recently created table accounts.

>>> db.check_table_exists('customers', 'email')
False

It returns False as there is no table customers in our database right now.

Deleting a table
----------------

>>> db.delete_table('accounts')

This will delete the table 'accounts' from our database.

Altering a table
----------------

>>> db.alter_table('accounts', 'ADD', 'phone VARCHAR(255)')
>>> db.alter_table('accounts', 'DROP', 'email')
>>> db.alter_table('accounts', 'MODIFY', 'phone INT')

The ADD and DROP statements are used to add and drop columns from a table. The MODIFY statement is used to modify the data type of a column.

Inserting data
--------------

>>> db.insert_table('accounts', 'id, name, email, password', [1, 'John Doe', 'email@example.com', '123456789'])

This will insert the data in the specified columns.

Here the data (1, John Doe, email@example.com, 123456789) will be inserted in the columns (id, name, email, password).

Updating table
--------------

>>> db.update_table('accounts', 'name', 'Dan', 'id', 1)

This will update the value of name column to Dan where id is 1. 

Selecting table
---------------

>>> table = db.select_table('accounts')
>>> print(table)
[(1, 'Dan', 'email@example.com', '123456789'), (2, 'Joe', 'email2@example.com', '930232213'), (3, 'Smith', 'email3@example.com', '232131231')]

This will return all the entries of a table in a list containing tuple of each row.

Selecting column
----------------

>>> column = db.select_column('accounts', 'name')
>>> print(column)
[('Dan',), ('Joe',), ('Smith',)]

This will return all entries of a column of the table.

Selecting data
--------------

>>> data = db.select_data('accounts', 'password', 'name', ['Dan'])
>>> print(data)
('123456789',)

This will return password of field where the name is Dan.

>>> data = db.select_data('accounts', 'password', 'id, name', [1, 'Dan'])
>>> print(data)
('123456789',)

This will return password of field where the id is 1 and name is Dan.

>>> row = db.select_row('accounts', '*', 'name', ['Dan'])
>>> print(row)
(1, 'Dan', 'email@example.com', '123456789')

\* means 'all'. This will return the row where name is Dan.

Deleting row
------------

>>> db.delete_row('accounts', 'name', ['Dan'])

This will delete the row where name is Dan.