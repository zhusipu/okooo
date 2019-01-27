from CommonModel import CommonModel

class RangqiuModel(CommonModel):
    def __init__(self):
        super(RangqiuModel, self).__init__()

    def save(self, rangqiu):
        self.cursor.execute("select id from rangqiu where `match` = %d and `company` = %d and rangqiu = %d"%(rangqiu['match'],rangqiu['company'],rangqiu['rangqiu']) )
        result = self.cursor.fetchone()
        if result == None:
            insertSql = u"INSERT INTO `rangqiu`(`match`, `company`, `rangqiu`, `zhushengzhishu`, `pingjuzhishu`, `keshengzhishu`, `newzhushengzhishu`, `newpingjuzhishu`, `newkeshengzhishu`, `newzhushenggailv`, `newpingjugailv`, `newkeshenggailv`, `newkailizhushengzhishu`, `newkailipingjuzhishu`, `newkailikeshengzhishu`, `peifulv`)  VALUES(%d, %d, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f)"%(rangqiu['match'],rangqiu['company'],rangqiu['rangqiu'],rangqiu['zhushengzhishu'],rangqiu['pingjuzhishu'],rangqiu['keshengzhishu'],rangqiu['newzhushengzhishu'],rangqiu['newpingjuzhishu'],rangqiu['newkeshengzhishu'],rangqiu['newzhushenggailv'],rangqiu['newpingjugailv'],rangqiu['newkeshenggailv'],rangqiu['newkailizhushengzhishu'],rangqiu['newkailipingjuzhishu'],rangqiu['newkailikeshengzhishu'],rangqiu['peifulv'])
            self.cursor.execute(insertSql)
        else:
            updateSql = u"UPDATE `rangqiu` SET `match` = %d, `company` = %d, `rangqiu` = %d, `zhushengzhishu` = %.2f, `pingjuzhishu` = %.2f, `keshengzhishu` = %.2f, `newzhushengzhishu` = %.2f, `newpingjuzhishu` = %.2f, `newkeshengzhishu` = %.2f, `newzhushenggailv` = %.2f, `newpingjugailv` = %.2f, `newkeshenggailv` = %.2f, `newkailizhushengzhishu` = %.2f, `newkailipingjuzhishu` = %.2f, `newkailikeshengzhishu` = %.2f, `peifulv` = %.2f WHERE `id` = %d"%(rangqiu['match'],rangqiu['company'],rangqiu['rangqiu'],rangqiu['zhushengzhishu'],rangqiu['pingjuzhishu'],rangqiu['keshengzhishu'],rangqiu['newzhushengzhishu'],rangqiu['newpingjuzhishu'],rangqiu['newkeshengzhishu'],rangqiu['newzhushenggailv'],rangqiu['newpingjugailv'],rangqiu['newkeshenggailv'],rangqiu['newkailizhushengzhishu'],rangqiu['newkailipingjuzhishu'],rangqiu['newkailikeshengzhishu'],rangqiu['peifulv'],result[0])
            self.cursor.execute(updateSql)
