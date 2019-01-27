from dbconfig import config
import MySQLdb as mdb
class CommonModel(object):
    def __init__(self):
        self.conn = mdb.connect(**config)
        self.cursor = self.conn.cursor()