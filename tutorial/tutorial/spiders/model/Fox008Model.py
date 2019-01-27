from CommonModel import CommonModel
import datetime

class Fox008Model(CommonModel):
    def __init__(self):
        super(Fox008Model, self).__init__()

    def save(self, fox008):
        self.cursor.execute("select id,zt from `fox008` where `match` = %d "%(fox008['match']) )
        result = self.cursor.fetchone()
        if result == None:
            insertSql = u"INSERT INTO `fox008`(`match`, `pk`, `zt`, `gl`) VALUES (%d, '%s', %d, %.2f)"%(fox008['match'],fox008['pk'], fox008['zt'], fox008['gl'])
            self.cursor.execute(insertSql)
            self.cursor.execute("select id,zt from `fox008` where `match` = %d "%(fox008['match']) )
            result = self.cursor.fetchone()
            now_time = datetime.datetime.now()
            date = (now_time).strftime('%Y-%m-%d %H:%M:%S')
            insertSql = u"INSERT INTO `fox008_change`(`fid`, `time`, `zt`) VALUES (%d, '%s', %d)"%(result[0], date, fox008['zt'])
            self.cursor.execute(insertSql)
        else:
            if result[1] != fox008['zt']:
                now_time = datetime.datetime.now()
                date = (now_time).strftime('%Y-%m-%d %H:%M:%S')
                insertSql = u"INSERT INTO `fox008_change`(`fid`, `time`, `zt`) VALUES (%d, '%s', %d)"%(result[0],date, fox008['zt'])
                self.cursor.execute(insertSql)
            updateSql = u"UPDATE `fox008` SET `pk` = '%s', `zt` = %d, `gl` = %.2f where id = %d"%(fox008['pk'], fox008['zt'], fox008['gl'], result[0])
            self.cursor.execute(updateSql)
