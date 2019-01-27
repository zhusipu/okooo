from CommonModel import CommonModel

class TeamModel(CommonModel):
    def __init__(self):
        super(TeamModel, self).__init__()
    
    def getTeamIdByName(self, name):
        self.cursor.execute("select id from team where name = '" + name + "'" )
        result = self.cursor.fetchone()
        if result == None:
            self.insertTeam(name)
            return self.getTeamIdByName(name)
        else:
            return result[0]
    
    def insertTeam(self, name):
        self.cursor.execute("INSERT INTO `team`(`name`) VALUES ('" + name + "')" )
