from CommonModel import CommonModel

class PeilvModel(CommonModel):
    def __init__(self):
        super(PeilvModel, self).__init__()

    def save(self, peilv):
        self.cursor.execute("select id from rangqiu where `match` = %d and `company` = %d "%(peilv['match'],peilv['company']) )
        result = self.cursor.fetchone()
        if result == None:
            insertSql = u"INSERT INTO `peilv` (`match`, `company`, `zz`, `pz`, `kz`) VALUES ('%d', '%d', '%.2f', '%.2f', '%.2f')"%(peilv['match'],peilv['company'],peilv['zz'],peilv['pz'],peilv['kz'])
            self.cursor.execute(insertSql)
        else:
            updateSql = u"UPDATE `peilv` SET `match`='%d', `company`='%d', `zz`='%.2f', `pz`='%.2f', `kz`='%.2f' WHERE (`id`='%d')"%(peilv['match'],peilv['company'],peilv['zz'],peilv['pz'],peilv['kz'],result[0])
            self.cursor.execute(updateSql)
