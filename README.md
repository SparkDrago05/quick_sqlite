# quick_sqlite

It is a fast package that will ease you to work with sqlite3.

## Installation
```
pip install quick_sqlite
```

## Usage
### Simple and Protected Database
```
from quick_sqlite import QuickSqlite
database_path = './data/example'
key = b'7vEREn9p76PwgOYxBY-ManCwy_XuYGFxKY0XtMBTF_E='
simple_database = QuickSqlite(database_path)
protected_database = QuickSqlite(database_path, True, key)
```

### Example
```
from quick_sqlite import QuickSqlite
qsql = QuickSqlite('example')
qsql.create_table('employes', 'name, email')
qsql.insert_table('employes', 'name, email', ['John', 'John@gmail.com'])
table = qsql.select_table('employes')
print(table)
```