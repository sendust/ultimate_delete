### Features

- Delete aged file, folder
- create auto delete table with sendust_table.py
- Table list should have 'path', 'age', 'recursive' header

#### Create path list Table

`python sendust_table.py`
```console
Available command list....
 ['new', 'file', 'edit', 'quit', 'exit', 'delete', 'help', 'save', 'load', 'header', 'show', 'data']
input command
..> header
header ----
[]
data ------
Please input header field [1]  path
Please input header field [2]  age
Please input header field [3]  recursive
Please input header field [4]
header ----
['path', 'age', 'recursive']
data ------
..> data
header ----
['path', 'age', 'recursive']
data ------
Input data for [path]  c:\temp
Input data for [age]  10
Input data for [recursive]  0
append table with data {'path': 'c:\\temp', 'age': '10', 'recursive': '0'}
Input data for [path]
header ----
['path', 'age', 'recursive']
data ------
0 -->  {'path': 'c:\\temp', 'age': '10', 'recursive': '0'}
..> file
Current file name is table.json
Please input new file name (without extension) testdata
New file name is testdata.json
..> save
save table..  [testdata.json]  record length 1
..> show
header ----
['path', 'age', 'recursive']
data ------
0 -->  {'path': 'c:\\temp', 'age': '10', 'recursive': '0'}
..>

```
#### Run delete script (test mode)
`
python ultimate_delete.py testdata.json
`


#### Run delete script (real mode)
`
python ultimate_delete.py testdata.json notest
`
