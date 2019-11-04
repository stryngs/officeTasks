# officeTasks
A collection of utilities I use in my 9-5, saving me significant time due to repetitive usage.

## Generic Class
#### Menu creation based on files in a directory
```
import officeTasks as OT

for i in range(10):
    c = open('{0}.csv'.format(i), 'w')
    c.close()
    x = open('{0}.xml'.format(i), 'w')
    x.close()

dList, tgtList = OT.gn.fileMenu(fileType = 'xml')
print('\n' + dList)
xmlFile = tgtList[int(input('XML Name?\n'))]
print('Your selected file was: {0}'.format(xmlFile))
```

#### Easy deletion of files or directories
```import officeTasks as OT
import os

c = open('exampleFile.csv', 'w')
c.close()

os.mkdir('foo')

OT.gnr.sweep('exampleFile.csv')
OT.gnr.sweep('foo')
OT.gnr.sweep('fileThatDoesNotExist')
```

### Csv Class
#### Easily create a CSV (Python3 right now -- Will add a Python2 option soon enough)
```
import officeTasks as OT

ourList = [('a', 'b', 'c'), (1, 2, 3), (4, 5, 6), ('d', 'e', 'f')]
headers = ['column a', 'column b', 'column c']

OT.csv.csvGen('my.csv', headers, ourList)
```

#### Take a CSV and make a List of Lists based on the rows (Python3 right now -- Will add a Python2 option soon enough)
```
import officeTasks as OT

myList = OT.csv.csv2list('my.csv')
```

#### Take a CSV and create a SQLite3 database from it
```
import officeTasks as OT

myCon = OT.csv.csv2sql('my.csv', 'mytable', 'my.sqlite3')
myCon.close()
```

#### Take a SQLite3 DB and create a CSV from a given table (Python3 right now -- Will add a Python2 option soon enough)
```
import officeTasks as OT

myCon = OT.csv.csv2sql('my.csv', 'mytable', 'my.sqlite3')
myCon.close()

OT.csv.sql2csv('new.csv', 'my.sqlite3', 'mytable')
```

#### Draft a quick email
```
import officeTasks as OT


OT.eml.wrapper()
    -or-
OT.eml.conDetails(server, username, password, debug = dbg, port = prt)
OT.eml.mxPrep(recipients, subject, body)
OT.eml.mxCon()
OT.eml.mxSend()
```
