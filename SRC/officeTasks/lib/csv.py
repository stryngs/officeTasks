import csv
import pandas as pd
import sqlite3 as lite

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
                    csvlist.append(row)
            return csvList


    def csv2sql(self, fName, tbName, dbName, df = False, compact = False, delim = ',', encoding = 'default'):
        """Turn the CSV to SQL

        Acts as a wrapper for Pandas read_csv()

        Returns the connection, you must close
        """
        ## Connect and create dataframe
        con = lite.connect(dbName)
        if df is not False:
            df = df
        else:
            if encoding == 'default':
                df = pd.read_csv(fName, sep = delim)
            else:
                df = pd.read_csv(fName, sep = delim, encoding = encoding)

        ## Let user compact column names
        if compact is True:
            df.columns = [c.replace(' ', '') for c in df.columns]

        ## SQL it
        df.to_sql(tbName,
                  con,
                  if_exists = 'append',
                  index = False)
        con.commit()
        return con


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
