from CommonModel import CommonModel

from lxml import etree
class ShangxiaModel(CommonModel):
    def __init__(self):
        super(ShangxiaModel, self).__init__()

    def save(self, shangxia):
        self.cursor.execute("select id from shangxia where `match` = %d and `company` = %d"%(shangxia['match'],shangxia['company']) )
        result = self.cursor.fetchone()
        if result == None:
            insertSql = u"INSERT INTO `shangxia`(`match`, `company`, `shangshui`, `pankou`, `xiashui`, `newshanghui`, `newpankou`, `newxiashui`, `newshangpangailv`, `newxiapangailv`, `newshangpankaili`, `newxiapankaili`, `peifulv`) VALUES (%d, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f)"%(shangxia['match'],shangxia['company'],shangxia['shangshui'],shangxia['pankou'],shangxia['xiashui'],shangxia['newshanghui'],shangxia['newpankou'],shangxia['newxiashui'],shangxia['newshangpangailv'],shangxia['newxiapangailv'],shangxia['newshangpankaili'],shangxia['newxiapankaili'],shangxia['peifulv'])
            self.cursor.execute(insertSql)
        else:
            updateSql = u"UPDATE `shangxia` SET `match` = %d, `company` = %d, `shangshui` =  %.2f, `pankou` =  %.2f, `xiashui` =  %.2f, `newshanghui` =  %.2f, `newpankou` =  %.2f, `newxiashui` =  %.2f, `newshangpangailv` =  %.2f, `newxiapangailv` =  %.2f, `newshangpankaili` =  %.2f, `newxiapankaili` =  %.2f, `peifulv` =  %.2f WHERE `id` =  %d"%(shangxia['match'],shangxia['company'],shangxia['shangshui'],shangxia['pankou'],shangxia['xiashui'],shangxia['newshanghui'],shangxia['newpankou'],shangxia['newxiashui'],shangxia['newshangpangailv'],shangxia['newxiapangailv'],shangxia['newshangpankaili'],shangxia['newxiapankaili'],shangxia['peifulv'],result[0])
            self.cursor.execute(updateSql)
