# excel2db
a tiny module that prepares *.xls, *.xlsx and *.csv files for their processing in sqlite3

The module ```0sql.py``` is supposed to be executed from the terminal:

```
>python -i 0sql.py
```

File system:

```
root_dir
|_0sql.py
|_databases
  |_*.xlsx
  |_*.xls
```

Once a new database has been created you can exit the interactive python session:
```
>>>exit()
```
Unfortunately i have not yet come up with a solution to terminate the session from within the python script. Might think about it later 
