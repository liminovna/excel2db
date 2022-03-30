import os
import pandas as pd
import sqlite3
import time
import sys


class Excel2Sql:
    
    def __init__(self):
        self.tables = filter(lambda f: not f.endswith('db'), os.listdir())
        self.tables_dict = self.populate_tables_dict(self.tables)
        self.active_files = None
        self.new_database = None

    def __str__(self) -> str:
        line = ""
        line += "\n"
        line += "-"*60
        line += "\nFile index: \n"

        for i in range(len(self.tables_dict)):
            line += "\t" + str(i) + ": " + self.tables_dict[str(i)] + "\n"

        line += "-"*60
        
        return line

    def populate_tables_dict(self, tables) -> dict:
        
        result = {}
        for index, table in enumerate(tables):
            result[str(index)] = table

        return result

    def choose_tables(self):
        wanted = []
        print('Please type in indices of the files you want to work with')
        while True:
            q = str(input("\t"))
            if q == "":
                return wanted
            try:
                wanted.append(self.tables_dict[q])
            except KeyError:
                print('\t^ Invalid key')
                continue

    def populate_database(self, db_name):
        self.new_database = sqlite3.connect(db_name)

        for file in self.active_files:
            if file.endswith('.xls') or file.endswith('.xlsx'):
                sheets = pd.read_excel(file, sheet_name=None)
            elif file.endswith('.csv'):
                sheets = pd.read_csv(file, delimiter=';', sheet_name=None)
            for table, df in sheets.items():
                df.to_sql(f'{file}__{table}'.replace(' ', ''), self.new_database)

        return self.new_database
    
    @staticmethod
    def list_dbs():
        res = filter(lambda f: f.endswith('db'), os.listdir())
        print(*res, sep='\n')


if __name__ == "__main__":

    if 'databases' not in os.getcwd():
        os.chdir('databases')
    
    print('Welcome! To see currently available databases run "list_dbs" command.')

    t_ = time.localtime()
    t = {
        'day': (2-len(str(t_.tm_mday)))*'0' + str(t_.tm_mday),
        'month': (2-len(str(t_.tm_mon)))*'0' + str(t_.tm_mon),
        'hour': (2-len(str(t_.tm_hour)))*'0' + str(t_.tm_hour),
        'min': (2-len(str(t_.tm_min)))*'0' + str(t_.tm_min)
    }
    resulting_db_name = f"{t['day']}-{t['month']}_{t['hour']}-{t['min']}.db" 

    dbs = Excel2Sql()
    print(dbs)
    dbs.active_files = dbs.choose_tables()

    con = dbs.populate_database(resulting_db_name)
    print(resulting_db_name + ' has been successfully created!')

