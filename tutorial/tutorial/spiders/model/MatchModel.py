from CommonModel import CommonModel
import datetime

class MatchModel(CommonModel):
    def __init__(self):
        super(MatchModel, self).__init__()
    
    def getMatchId(self, key, name, matchType, matchTime, homeTeam, homeTeamFen, visitingTeam, visitingTeamFen, result):
        self.cursor.execute("select id from `match` where `key` = '" + key + "'" )
        dbResult = self.cursor.fetchone()
        if dbResult == None:
            self.insertMatch(key, name, matchType, matchTime, homeTeam, homeTeamFen, visitingTeam, visitingTeamFen, result)
            return self.getMatchId(key, name, matchType, matchTime, homeTeam, homeTeamFen, visitingTeam, visitingTeamFen, result)
        else:
            self.updateMatch(dbResult[0], homeTeamFen, visitingTeamFen, result)
            return dbResult[0]
    
    def getMatchIdByKey(self, key):
        self.cursor.execute("select id from `match` where `key` = '" + key + "'" )
        result = self.cursor.fetchone()
        if result == None:
            return None
        else:
            return result[0]
            
    def updateSyncTime(self):
        syncTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("update `sys` set `syncTime` = '" + str(syncTime) + "' where id = 1")
        
    def insertMatch(self, key, name, matchType, matchTime, homeTeam, homeTeamFen, visitingTeam, visitingTeamFen, result):
        self.cursor.execute("INSERT INTO `match`(`key`, `name`, `matchType`, `matchTime`, `homeTeam`, `homeTeamFen`, `visitingTeam`, `visitingTeamFen`, `result`) VALUES ('" + key + "', '" + name + "', " + str(matchType) + ", '" + matchTime + "', " + str(homeTeam) + ", " + str(homeTeamFen) + ", " + str(visitingTeam) + ", " + str(visitingTeamFen) + " , " + str(result) + " ) " )

    def updateMatch(self, id, homeTeamFen, visitingTeamFen, result):
        updateSql = "update `match` set `homeTeamFen` = " + str(homeTeamFen) + ", `visitingTeamFen` = " + str(visitingTeamFen) + ", `result` = " + str(result) + " where id = " + str(id) + " "
        self.cursor.execute(updateSql)