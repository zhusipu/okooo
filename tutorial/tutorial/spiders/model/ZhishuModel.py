from CommonModel import CommonModel

class ZhishuModel(CommonModel):
    def __init__(self):
        super(ZhishuModel, self).__init__()

    def save(self, zhishu):
        self.cursor.execute("select id from zhishu where `match` = %d"%(zhishu['match']) )
        result = self.cursor.fetchone()
        if result == None:
            insertSql = u"INSERT INTO `zhishu`(`match`, `defaultMainVictoryIndex`, `defaultDrawIndex`, `defaultGuestWinsIndex`, `newMainVictoryIndex`, `newDrawIndex`, `newGuestWinsIndex`, `remind`) VALUES (%d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, '%s')"%(zhishu['match'], zhishu['defaultMainVictoryIndex'], zhishu['defaultDrawIndex'], zhishu['defaultGuestWinsIndex'], zhishu['newMainVictoryIndex'], zhishu['newDrawIndex'], zhishu['newGuestWinsIndex'], zhishu['remind'])
            self.cursor.execute(insertSql)
        else:
            updateSql = u"UPDATE `zhishu` SET `match` = '%d', `defaultMainVictoryIndex` = %.2f, `defaultDrawIndex` = %.2f, `defaultGuestWinsIndex` = %.2f, `newMainVictoryIndex` = %.2f, `newDrawIndex` = %.2f, `newGuestWinsIndex` = %.2f, `remind` = '%s' WHERE `id` = %d"%(zhishu['match'], zhishu['defaultMainVictoryIndex'], zhishu['defaultDrawIndex'], zhishu['defaultGuestWinsIndex'], zhishu['newMainVictoryIndex'], zhishu['newDrawIndex'], zhishu['newGuestWinsIndex'], zhishu['remind'], result[0])

            self.cursor.execute(updateSql)
