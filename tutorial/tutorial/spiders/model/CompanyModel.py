from CommonModel import CommonModel

class CompanyModel(CommonModel):
    def __init__(self):
        super(CompanyModel, self).__init__()
    
    def getCompanyIdByName(self, name):
        self.cursor.execute("select id from company where name = '" + name + "'" )
        result = self.cursor.fetchone()
        if result == None:
            self.insertCompany(name)
            return self.getCompanyIdByName(name)
        else:
            return result[0]
    
    def insertCompany(self, name):
        self.cursor.execute("INSERT INTO `company`(`name`) VALUES ('" + name + "')" )
