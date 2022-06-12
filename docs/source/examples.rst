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

>>> from quick_sqlite import Column
>>> db.create_table('accounts', [Column('id', 'INT'), Column('name', 'VARCHAR(255)'), Column('email', 'VARCHAR(255)'), Column('password', 'VARCHAR(255)')])

Here table name is 'accounts' and columns are 'id', 'name', 'email' and 'password'.
The Column class is imported from quick_sqlite package and its first arguement is column name and the second arguement is column data type.

Renaming a table
----------------

>>> db.rename_table('accounts', 'users')
>>> db.rename_table('users', 'accounts')

First line will change name of the table 'accounts' to 'users'.
Second line will change it back to 'accounts'


Checking for a table
--------------------

>>> db.check_table_exists('accounts')
True

It returns True as we just recently created table accounts.

>>> db.check_table_exists('customers')
False

It returns False as there is no table customers in our database right now.

Deleting a table
----------------

>>> db.delete_table('accounts')

This will delete the table 'accounts' from our database.

Inserting data
--------------

.. code-block:: python

    data = {
    'id': 1,
    'name': 'John Doe',
    'email': 'email@example.com',
    'password': '123456789'
    }
    db.insert_data('accounts', data)

This will insert the data in the specified columns.

Here the data is provided as a dictionary where the key is column name and the value is column data.

Updating data
--------------

.. code-block:: python

    data = {
    'name': 'Dan',
    }
    db.update_data('accounts', data, 'id', 1)

This will update the value of name column to Dan where id is 1. 

Fetching a table
----------------

>>> table = db.fetch_table('accounts')
>>> print(table)
[(1, 'Dan', 'email@example.com', '123456789'), (2, 'Joe', 'email2@example.com', '930232213'), (3, 'Smith', 'email3@example.com', '232131231')]

This will return all the entries of a table in a list containing tuple of each row.

If you want specific number of rows then use **row_limit** arguement.

>>> limited_table = db.fetch_table('accounts', 2)
>>> print(limited_table)
[(1, 'Dan', 'email@example.com', '123456789'), (2, 'Joe', 'email2@example.com', '930232213')]

Adding a column
---------------

>>> from quick_sqlite import Column
>>> db.add_column('accounts', Column('address', 'VARCHAR(255)'))

This will create a new column 'address' with data type 'VARCHAR' in table 'accounts'.

Renaming a column
-----------------

>>> db.rename_column('accounts', 'address', 'home address')

This will rename column 'address' to 'home address' in table 'accounts'.

Deleting a column
-----------------

>>> db.delete_column('accounts', 'home address')

This will delete column 'home address' in table 'accounts'.

Selecting column
----------------

>>> column = db.fetch_column('accounts', 'name')
>>> print(column)
[('Dan',), ('Joe',), ('Smith',)]

This will return all entries of a column of the table.

Checking for a column
---------------------

>>> db,check_column_exists('accounts', 'name')
True
>>> db,check_column_exists('accounts', 'address')
False

This will check if a column exists in the table.

Selecting data
--------------

>>> data = db.fetch_data('accounts', 'password', 'name', 'Dan', '=')
>>> print(data)
('123456789',)

This will return password of field where the name is equal to Dan.

>>> data = db.fetch_data('accounts', 'password', 'id', '1', '>')
>>> print(data)
None

This will return password of field where the id is greater than 1 

The supported consitions are: =, <, >, <=, >=, <>(not equal).

The statement will look like: {filter_column_name} {condition} {filter_column_data}

Deleting row
------------

>>> db.delete_row('accounts', 'name', 'Dan')

This will delete the row where name is Dan.