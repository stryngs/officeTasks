import csv
import re
import sqlite3 as lite
from datetime import datetime

class Csv(object):
    """All things, csv related"""

    def csvGen(self, csvName, headers, rows, delim = ',', quoteChar = '"', encoding = 'default'):
        """Gen the CSV

        Uses settings of:
            , for delimiter - by Default
            " for quoting chararacter - by Default
            QUOTE_MIMINAL
        """
        if encoding == 'default':
            with open(csvName, 'w', newline = '') as oFile:
                csv_out = csv.writer(oFile,
                                     delimiter = delim,
                                     quotechar = quoteChar,
                                     quoting = csv.QUOTE_MINIMAL)
                csv_out.writerow(headers)
                for row in rows:
                    self.ourRow = row
                    csv_out.writerow(row)
        else:
            with open(csvName, 'w', newline = '', encoding = encoding) as oFile:
                csv_out = csv.writer(oFile,
                                     delimiter = delim,
                                     quotechar = quoteChar,
                                     quoting = csv.QUOTE_MINIMAL)
                csv_out.writerow(headers)
                for row in rows:
                    self.ourRow = row
                    csv_out.writerow(row)


    def csvYield(self, csvFile, delim = ',', quoteChar = '"'):
        """ Yields a row from a given CSV

        Uses defaults of:
            , for delimiter - by Default
            " for quoting chararacter - by Default

        Need to look deeper into newline and if it is needed at all, or if conflict
        might be caused by having it...
        """
        with open(csvFile, 'r', newline = '') as iFile:
            rows = csv.reader(iFile,
                              delimiter = delim,
                              quotechar = quoteChar)

            ## Iterate through rows
            for row in rows:
                yield row


    def csv2list(self, fName, delim = ',', quoteChar = '"', encoding = 'default'):
        """Turn the CSV into a list of lists where each list is a given row"""
        csvList = []
        if encoding == 'default':
            with open(fName, 'r') as iFile:
                rows = csv.reader(iFile,
                                  delimiter = delim,
                                  quotechar = quoteChar)
                for row in rows:
                    csvList.append(row)
            return csvList
        else:
            with open(fName, 'r', encoding = encoding) as iFile:
                rows = csv.reader(iFile,
                                  delimiter = delim,
                                  quotechar = quoteChar)
                for row in rows:
                    csvList.append(row)
            return csvList


    def csv2sql(self, fName, tbName, dbName, delim = '.', encoding = 'default'):
        """Turn the CSV to SQL

        Attempts data detection based off the first row of data

        Returns the connection, you must close
        """
        con = lite.connect(dbName)
        db = con.cursor()

        with open(fName) as csv_file:
            rows = list(csv.reader(csv_file))
        hdrs = [i.replace(' ', '') for i in rows.pop(0)]
        hdrs = [f'`{i}`' for i in hdrs]                                        ## Deal with reserved columns

        ## Attempt determinations
        if len(rows) >= 1:
            guesses = [self.guessType(value) for value in rows[0]]
            # q = f'''CREATE TABLE IF NOT EXISTS {tbName} (id INTEGER PRIMARY KEY, {", ".join(f"{col} {dtype}" for col, dtype in zip(hdrs, guesses))})
            #      '''
            q = f'''CREATE TABLE IF NOT EXISTS {tbName} ({", ".join(f"{col} {dtype}" for col, dtype in zip(hdrs, guesses))})
                 '''
            db.execute(q)

            ## SQL it
            for row in rows:
                insert_query = f'INSERT INTO {tbName} ({", ".join(hdrs)}) VALUES ({", ".join(["?"] * len(hdrs))})'
                db.execute(insert_query, tuple(row))
            con.commit()
        return con


    def guessType(self, value):
        """Attempts to guess the input type and returns text by default"""
        if re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            try:
                datetime.strptime(value, '%Y-%m-%d')
                return 'DATE'
            except:
                pass
        elif re.match(r'^\d+$', value):
            return 'INTEGER'
        elif re.match(r'^\d+\.\d+$', value):
            return 'REAL'
        return 'TEXT'


    def sql2csv(self, csvName, dbName, tbName, delim = ',', quoteChar = '"', encoding = 'default'):
        """Take a SQL table, and dump to CSV

        Uses settings of:
            , for delimiter - by Default
            " for quoting chararacter - by Default
            QUOTE_MIMINAL
        """
        con = lite.connect(dbName)
        db = con.cursor()
        q = db.execute('SELECT * FROM "{0}"'.format(tbName))
        headers = list(map(lambda x: x[0], q.description))
        rows = q.fetchall()
        con.close()
        self.csvGen(csvName,
                    headers,
                    rows,
                    delim = delim,
                    quoteChar = quoteChar,
                    encoding = encoding)
