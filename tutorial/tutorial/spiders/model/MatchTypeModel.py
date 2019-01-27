from CommonModel import CommonModel

class MatchTypeModel(CommonModel):
    def __init__(self):
        super(MatchTypeModel, self).__init__()
    
    def getMatchTypeIdByName(self, name):
        self.cursor.execute("select id from match_type where name = '" + name + "'" )
        result = self.cursor.fetchone()
        if result == None:
            self.insertMatchType(name)
            return self.getMatchTypeIdByName(name)
        else:
            return result[0]
    
    def insertMatchType(self, name):
        self.cursor.execute("INSERT INTO `match_type`(`name`) VALUES ('" + name + "')" )
