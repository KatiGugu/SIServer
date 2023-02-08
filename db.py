'''
A module that provides a class for interacting with a database.
'''
import sqlite3


class dbase():
    def __init__(self):
        self.cursor, self.conection = self.create_table()

    def create_table(self):
        '''
        Creates a database file with a table to store system information.
        Returns cursor and connection objects
        '''
        try:
            with sqlite3.connect('sysinfo.db') as db:
                db.execute('CREATE TABLE IF NOT EXISTS sysinfo '
                           '(date integer, sysdata text)')
                db.commit()
                cursor = db.cursor()
                return cursor, db
        except KeyError:
            return None, None

    def save_to_db(self, time, data):
        '''
        Saves information in database
        '''
        self.cursor.execute('INSERT INTO sysinfo VALUES (?, ?)',
                            (time, data))

    def retrive_from_db(self, time1, time2):
        '''
        Retrives information from database
        '''
        self.cursor.execute("SELECT * FROM sysinfo WHERE date >= ? AND date \
                            <= ?", (time1, time2,))
        sysdata = self.cursor.fetchall()
        return sysdata

    def clear_db(self):
        '''
        Deletes all records in database
        '''
        self.cursor.execute("DELETE FROM sysinfo")

    def del_records(self, time):
        '''
        Delets records with vallume date less than "time".
        '''
        self.cursor.execute("DELETE FROM sysinfo WHERE date < ?", (time,))

    def time_of_first_rec(self):
        '''
        Returns the entry with the smallest date value
        '''
        self.cursor.execute("SELECT date FROM sysinfo ORDER BY date LIMIT 1")
        return self.cursor.fetchone()
