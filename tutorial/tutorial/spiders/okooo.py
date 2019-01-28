# -*- coding: utf-8 -*-
import scrapy
import json
from model import TeamModel
from model import MatchTypeModel
from model import MatchModel
from model import ZhishuModel
from model import CompanyModel
from model import ShangxiaModel
from model import RangqiuModel
from model import Fox008Model
from model import PeilvModel
from lxml import etree
from utils import resultToFormat
import time
import datetime
from pandas.tseries.offsets import Day
import sys
 
reload(sys)
sys.setdefaultencoding('utf8')
class OkoooSpider(scrapy.Spider):
    name = "okooo"
    year = time.strftime('%Y',time.localtime(time.time()))
    c = 100
    week_day_dict = {
      0 : '周一',
      1 : '周二',
      2 : '周三',
      3 : '周四',
      4 : '周五',
      5 : '周六',
      6 : '周日',
    }
    def start_requests(self):
        matchModel = MatchModel()
        matchModel.updateSyncTime()
        now_time = datetime.datetime.now()
        # i = 0
        # while i <= self.c:
        #     date = (now_time - i * Day()).strftime('%Y%m%d')
        #     yield scrapy.Request(url='https://m.fox008.com/mobile/dataCatList?playType=YP&matchDate=' + date, meta={'date':date}, callback=self.parseFox)
        #     i = i + 1
        # i = 0  
        # while i < 2:
        #     date = (now_time + i * Day()).strftime('%Y%m%d')
        #     yield scrapy.Request(url='https://m.fox008.com/mobile/dataCatList?playType=YP&matchDate=' + date, meta={'date':date}, callback=self.parseFox)
        #     i = i + 1
        # i = 0
        # while i < self.c:
        #   date = (now_time - i * Day()).strftime('%Y-%m-%d')
        #   yd = (now_time - i * Day()).strftime('%Y-%m-%d')
        #   rc1 = (now_time - (i - 1) * Day()).strftime('%Y-%m-%d')
        #   rc2 = (now_time - (i - 2) * Day()).strftime('%Y-%m-%d')
        #   rc3 = (now_time - (i - 3) * Day()).strftime('%Y-%m-%d')
        #   yield scrapy.Request(url='http://www.okooo.com/jingcai/shuju/zhishu/' + date + '/', meta={'date':date, 'yd': yd, 'rc1': rc1, 'rc2': rc2, 'rc3': rc3}, callback=self.parse)
        #   i = i + 1
        
        # i = 0
        # while i < 3:
        #   date = (now_time + i * Day()).strftime('%Y-%m-%d')
        #   yd = (now_time - i * Day()).strftime('%Y-%m-%d')
        #   rc1 = (now_time - (i - 1) * Day()).strftime('%Y-%m-%d')
        #   rc2 = (now_time - (i - 2) * Day()).strftime('%Y-%m-%d')
        #   rc3 = (now_time - (i - 3) * Day()).strftime('%Y-%m-%d')
        #   yield scrapy.Request(url='http://www.okooo.com/jingcai/shuju/zhishu/' + date + '/', meta={'date':date, 'yd': yd, 'rc1': rc1, 'rc2': rc2, 'rc3': rc3}, callback=self.parse)
        #   i = i + 1

        # i = 0
        # while i < self.c:
        #   date = (now_time - i * Day()).strftime('%Y-%m-%d')
        #   yd = (now_time - i * Day()).strftime('%Y-%m-%d')
        #   rc1 = (now_time - (i - 1) * Day()).strftime('%Y-%m-%d')
        #   rc2 = (now_time - (i - 2) * Day()).strftime('%Y-%m-%d')
        #   rc3 = (now_time - (i - 3) * Day()).strftime('%Y-%m-%d')
        #   yield scrapy.Request(url='http://www.okooo.com/jingcai/shuju/shangxia/' + date + '/', meta={'date':date, 'yd': yd, 'rc1': rc1, 'rc2': rc2, 'rc3': rc3}, callback=self.parsmShangxiaPage)
        #   i = i + 1

        # i = 0
        # while i < self.c:
        #   date = (now_time - i * Day()).strftime('%Y-%m-%d')
        #   yd = (now_time - i * Day()).strftime('%Y-%m-%d')
        #   rc1 = (now_time - (i - 1) * Day()).strftime('%Y-%m-%d')
        #   rc2 = (now_time - (i - 2) * Day()).strftime('%Y-%m-%d')
        #   rc3 = (now_time - (i - 3) * Day()).strftime('%Y-%m-%d')
        #   yield scrapy.Request(url='http://www.okooo.com/jingcai/shuju/rangqiu/' + date + '/', meta={'date':date, 'yd': yd, 'rc1': rc1, 'rc2': rc2, 'rc3': rc3}, callback=self.parsmRangqiuPage)
        #   i = i + 1

        i = 0
        while i < self.c:
          date = (now_time - i * Day()).strftime('%Y-%m-%d')
          yd = (now_time - i * Day()).strftime('%Y-%m-%d')
          rc1 = (now_time - (i - 1) * Day()).strftime('%Y-%m-%d')
          rc2 = (now_time - (i - 2) * Day()).strftime('%Y-%m-%d')
          rc3 = (now_time - (i - 3) * Day()).strftime('%Y-%m-%d')
          yield scrapy.Request(url='http://www.okooo.com/jingcai/shuju/peilv/' + date + '/', meta={'date':date, 'yd': yd, 'rc1': rc1, 'rc2': rc2, 'rc3': rc3}, callback=self.parsmPeilvPage)
          i = i + 1

    def parseFox(self, response):
        data = json.loads(response.body)
        if 'data' not in data:
            return
        data = data['data']
        matchModel = MatchModel()
        fox008Model = Fox008Model()
        for item in data:
            matchKey = item['matchKeyWith_'][0:8] + item['matchKeyWith_'][-3:]
            match = matchModel.getMatchIdByKey(matchKey)
            if match == None:
                continue
            pk = item['pk'][0]
            zt = int(item['zt']) + 1
            gl = self.myFloat(item['gl'])
            fox008 = {
                'match':match,
                'pk':pk,
                'zt':zt,
                'gl':gl
            }
            fox008Model.save(fox008)
            

            
    def parsmShangxiaPage(self, response):
        page = int(response.xpath("//div[@class='pagination']//table//tr//td//span/text()")[1].extract())
        i = 1
        while i <= page:
            yield scrapy.Request(url='http://www.okooo.com/jingcai/shuju/shangxia/'+response.meta['date']+'/?PageID=' + str(i), meta=response.meta, callback=self.parseShangxia)
            i = i + 1

    def parsmRangqiuPage(self, response):
        page = int(response.xpath("//div[@class='pagination']//table//tr//td//span/text()")[1].extract())
        i = 1
        while i <= page:
            yield scrapy.Request(url='http://www.okooo.com/jingcai/shuju/rangqiu/'+response.meta['date']+'/?PageID=' + str(i), meta=response.meta, callback=self.parseRangqiu)
            i = i + 1

    def parsmPeilvPage(self, response):
        page = int(response.xpath("//div[@class='pagination']//table//tr//td//span/text()")[1].extract())
        i = 1
        while i <= page:
            yield scrapy.Request(url='http://www.okooo.com/jingcai/shuju/peilv/'+response.meta['date']+'/?PageID=' + str(i), meta=response.meta, callback=self.parsePeilv)
            i = i + 1

    def parse(self, response):
        data = response.xpath("//table[@class='magazine_table']//tr")
        teamModel = TeamModel()
        matchTypeModel = MatchTypeModel()
        zhishuModel = ZhishuModel()
        matchModel = MatchModel()
        for i in data:
            itemData = i.xpath("td").extract()
            if len(itemData) <> 16:
                continue
            [serialNumber, matchType, matchTime, homeTeam, draw, visitingTeam, defaultMainVictoryIndex, defaultDrawIndex, defaultGuestWinsIndex, newMainVictoryIndex, newDrawIndex, newGuestWinsIndex, remind, result, tmp1, tmp2 ] = i.xpath("td").extract()
            homeTeam = etree.HTML(homeTeam).xpath("//span/text()")[0]
            homeTeam = teamModel.getTeamIdByName(homeTeam)
            draw = (etree.HTML(draw).xpath("//td//span/text()"))
            homeTeamFen = 0
            visitingTeamFen = 0
            if len(draw) > 0:
                drawSplit = draw[0].split('-')
                if len(drawSplit) == 2:
                    homeTeamFen = self.myFloat(drawSplit[0])
                    visitingTeamFen = self.myFloat(drawSplit[1])
                
            newMainVictoryIndex = self.myFloat(etree.HTML(newMainVictoryIndex).xpath("//span/text()")[0])
            newDrawIndex = self.myFloat(etree.HTML(newDrawIndex).xpath("//span/text()")[0])
            newGuestWinsIndex = self.myFloat(etree.HTML(newGuestWinsIndex).xpath("//span/text()")[0])
            matchTime = etree.HTML(matchTime).xpath("//td/text()")[0]
            year = None
            if matchTime[:5] == response.meta['yd'][-5:]:
                year = response.meta['yd'][:4]
            elif matchTime[:5] == response.meta['rc1'][-5:]:
                year = response.meta['rc1'][:4]
            elif matchTime[:5] == response.meta['rc2'][-5:]:
                year = response.meta['rc2'][:4]
            elif matchTime[:5] == response.meta['rc3'][-5:]:
                year = response.meta['rc3'][:4]
            else:
                continue
            matchTime = year + '-' + matchTime + ':00'
            result = etree.HTML(result).xpath("//td/text()")
            if len(result) > 0:
                result = resultToFormat(result[0])
            else:
                result = 0
            defaultGuestWinsIndex =  self.myFloat(etree.HTML(defaultGuestWinsIndex).xpath("//td/text()")[0])
            defaultDrawIndex =  self.myFloat(etree.HTML(defaultDrawIndex).xpath("//td/text()")[0])
            visitingTeam = etree.HTML(visitingTeam).xpath("//span/text()")[0]
            visitingTeam = teamModel.getTeamIdByName(visitingTeam)
            defaultMainVictoryIndex = self.myFloat(etree.HTML(defaultMainVictoryIndex).xpath("//td/text()")[0])
            serialNumber = etree.HTML(serialNumber).xpath("//td/text()")[0]
            remind = etree.HTML(remind).xpath("//td//a/text()")
            newRemind = ""
            for ri in remind:
                newRemind = newRemind + str(resultToFormat(ri)) + ","
            matchType = etree.HTML(matchType).xpath("//span/text()")
            if len(matchType) > 0:
                matchType = matchType[0]
            else:
                matchType = '-'
            matchType = matchTypeModel.getMatchTypeIdByName(matchType)
            if self.get_week_day(datetime.datetime.strptime(matchTime[0:10], '%Y-%m-%d')) == serialNumber[0:2]:
                matchKey = matchTime[:4] + matchTime[5:7] + matchTime[8:10] + serialNumber[-3:]
            else:
                ## 判断前两天是否满足
                g = -2
                mingzhongdate = None
                while g < 2:
                    tmpdate = datetime.datetime.strptime(matchTime[0:10], '%Y-%m-%d')
                    tmpdate = (tmpdate + g * Day())
                    if self.get_week_day(tmpdate) ==  serialNumber[0:2]:
                        mingzhongdate = tmpdate
                        break
                    g = g + 1
                if mingzhongdate == None:
                    continue
                else:
                    mingzhongdate = datetime.datetime.strftime(mingzhongdate, "%Y%m%d")
                    matchKey = mingzhongdate + serialNumber[-3:]
            match = matchModel.getMatchId(matchKey, serialNumber, matchType, matchTime, homeTeam, homeTeamFen, visitingTeam, visitingTeamFen, result)
            zhishu = {
                'serialNumber':serialNumber,
                'match':match,
                'defaultMainVictoryIndex':defaultMainVictoryIndex,
                'defaultDrawIndex':defaultDrawIndex,
                'defaultGuestWinsIndex':defaultGuestWinsIndex,
                'newMainVictoryIndex':newMainVictoryIndex,
                'newDrawIndex':newDrawIndex,
                'newGuestWinsIndex':newGuestWinsIndex,
                'remind':newRemind[:-1]
            }
            zhishuModel.save(zhishu)
        
    def parseShangxia(self, response):
        data = response.xpath("//div[@class='clearfix container_wrapper pankoudata']")
        matchModel = MatchModel()
        companyModel = CompanyModel()
        shangxiaModel = ShangxiaModel()
        for i in data:
            matchName = i.xpath("div//p//b/text()")[0].extract()
            matchTime = i.xpath("div//p//b")[2].extract()
            matchTime = etree.HTML(matchTime).xpath("//b/text()")
            year = None
            if matchTime[0][:5] == response.meta['yd'][-5:]:
                year = response.meta['yd'][:4]
            elif matchTime[0][:5] == response.meta['rc1'][-5:]:
                year = response.meta['rc1'][:4]
            elif matchTime[0][:5] == response.meta['rc2'][-5:]:
                year = response.meta['rc2'][:4]
            elif matchTime[0][:5] == response.meta['rc3'][-5:]:
                year = response.meta['rc3'][:4]
            else:
                continue
            matchTime = year + '-' + matchTime[0] + ':00'
            if self.get_week_day(datetime.datetime.strptime(matchTime[0:10], '%Y-%m-%d')) == matchName[0:2]:
                matchKey = matchTime[:4] + matchTime[5:7] + matchTime[8:10] + matchName[-3:]
                pass
            else:
                ## 判断前两天是否满足
                g = -2
                mingzhongdate = None
                while g < 2:
                    tmpdate = datetime.datetime.strptime(matchTime[0:10], '%Y-%m-%d')
                    tmpdate = (tmpdate + g * Day())
                    if self.get_week_day(tmpdate) ==  matchName[0:2]:
                        mingzhongdate = tmpdate
                        break
                    g = g + 1
                if mingzhongdate == None:
                    continue
                else:
                    mingzhongdate = datetime.datetime.strftime(mingzhongdate, "%Y%m%d")
                    matchKey = mingzhongdate + matchName[-3:]
            match = matchModel.getMatchIdByKey(matchKey)
            if match == None:
                continue
            
            list = i.xpath("table//tr")

            e = 0
            for item in list:
                e = e + 1
                if e < 3:
                    continue
                (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12) = item.xpath("td").extract()
                # v1 = item.xpath("td").extract()
                company = etree.HTML(v1).xpath("//td/text()")[0]
                company = companyModel.getCompanyIdByName(company)
                shangshui = self.myFloat(etree.HTML(v2).xpath("//td/text()")[0])
                pankou = self.myFloat(etree.HTML(v3).xpath("//td/text()")[0])
                xiashui = self.myFloat(etree.HTML(v4).xpath("//td/text()")[0])
                newshanghui = self.myFloat(etree.HTML(v5).xpath("//td//span//span/text()")[0])
                newpankou = self.myFloat(etree.HTML(v6).xpath("//td//span//span/text()")[0])
                newxiashui = self.myFloat(etree.HTML(v7).xpath("//td//span//span/text()")[0])
                newshangpangailv = self.myFloat(etree.HTML(v8).xpath("//td/text()")[0])
                newxiapangailv = self.myFloat(etree.HTML(v9).xpath("//td/text()")[0])
                newshangpankaili = self.myFloat(etree.HTML(v10).xpath("//td//span//text()")[0])
                newxiapankaili = self.myFloat(etree.HTML(v11).xpath("//td/text()")[0])
                peifulv = self.myFloat(etree.HTML(v12).xpath("//td/text()")[0])
                shangxia = {
                    'match':match,
                    'company':company,
                    'shangshui':shangshui,
                    'pankou':pankou,
                    'xiashui':xiashui,
                    'newshanghui':newshanghui,
                    'newpankou':newpankou,
                    'newxiashui':newxiashui,
                    'newshangpangailv':newshangpangailv,
                    'newxiapangailv':newxiapangailv,
                    'newshangpankaili':newshangpankaili,
                    'newxiapankaili':newxiapankaili,
                    'peifulv':peifulv,
                }
                shangxiaModel.save(shangxia)
                
    def myFloat(self, val):
        if val == '-':
            return 0
        else:
            return float(val)

    def parseRangqiu(self, response):
        data = response.xpath("//div[@class='clearfix container_wrapper pankoudata']")
        matchModel = MatchModel()
        companyModel = CompanyModel()
        rangqiuModel = RangqiuModel()
        for i in data:
            matchName = i.xpath("div//p//b/text()")[0].extract()
            matchTime = i.xpath("div//p//b")[2].extract()
            matchTime = etree.HTML(matchTime).xpath("//b/text()")
            year = None
            if matchTime[0][:5] == response.meta['yd'][-5:]:
                year = response.meta['yd'][:4]
            elif matchTime[0][:5] == response.meta['rc1'][-5:]:
                year = response.meta['rc1'][:4]
            elif matchTime[0][:5] == response.meta['rc2'][-5:]:
                year = response.meta['rc2'][:4]
            elif matchTime[0][:5] == response.meta['rc3'][-5:]:
                year = response.meta['rc3'][:4]
            else:
                continue
            matchTime = year + '-' + matchTime[0] + ':00'
            if self.get_week_day(datetime.datetime.strptime(matchTime[0:10], '%Y-%m-%d')) == matchName[0:2]:
                matchKey = matchTime[:4] + matchTime[5:7] + matchTime[8:10] + matchName[-3:]
                pass
            else:
                ## 判断前两天是否满足
                g = -2
                mingzhongdate = None
                while g < 2:
                    tmpdate = datetime.datetime.strptime(matchTime[0:10], '%Y-%m-%d')
                    tmpdate = (tmpdate + g * Day())
                    if self.get_week_day(tmpdate) ==  matchName[0:2]:
                        mingzhongdate = tmpdate
                        break
                    g = g + 1
                if mingzhongdate == None:
                    continue
                else:
                    mingzhongdate = datetime.datetime.strftime(mingzhongdate, "%Y%m%d")
                    matchKey = mingzhongdate + matchName[-3:]
            match = matchModel.getMatchIdByKey(matchKey)
            if match == None:
                continue
            
            list = i.xpath("table//tr")

            e = 0
            for item in list:
                e = e + 1
                if e < 3:
                    continue
                (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15) = item.xpath("td").extract()
                company = etree.HTML(v1).xpath("//td/text()")[0]
                company = companyModel.getCompanyIdByName(company)
                rangqiu = int(etree.HTML(v2).xpath("//td/text()")[0])
                zhushengzhishu = self.myFloat(etree.HTML(v3).xpath("//td/text()")[0])
                pingjuzhishu = self.myFloat(etree.HTML(v4).xpath("//td/text()")[0])
                keshengzhishu = self.myFloat(etree.HTML(v5).xpath("//td/text()")[0])
                newzhushengzhishu = self.myFloat(etree.HTML(v6).xpath("//td//span/text()")[0])
                newpingjuzhishu = self.myFloat(etree.HTML(v7).xpath("//td//span/text()")[0])
                newkeshengzhishu = self.myFloat(etree.HTML(v8).xpath("//td//span/text()")[0])
                newzhushenggailv = self.myFloat(etree.HTML(v9).xpath("//td/text()")[0])
                newpingjugailv = self.myFloat(etree.HTML(v10).xpath("//td/text()")[0])
                newkeshenggailv = self.myFloat(etree.HTML(v11).xpath("//td/text()")[0])
                newkailizhushengzhishu = self.myFloat(etree.HTML(v12).xpath("//td//span/text()")[0])
                newkailipingjuzhishu = self.myFloat(etree.HTML(v13).xpath("//td//span/text()")[0])
                newkailikeshengzhishu = self.myFloat(etree.HTML(v14).xpath("//td//span/text()")[0])
                peifulv = self.myFloat(etree.HTML(v15).xpath("//td//text()")[0])
                rangqiu = {
                    'match':match,
                    'company':company,
                    'rangqiu':rangqiu,
                    'zhushengzhishu':zhushengzhishu,
                    'pingjuzhishu':pingjuzhishu,
                    'keshengzhishu':keshengzhishu,
                    'newzhushengzhishu':newzhushengzhishu,
                    'newpingjuzhishu':newpingjuzhishu,
                    'newkeshengzhishu':newkeshengzhishu,
                    'newzhushenggailv':newzhushenggailv,
                    'newpingjugailv':newpingjugailv,
                    'newkeshenggailv':newkeshenggailv,
                    'newkailizhushengzhishu':newkailizhushengzhishu,
                    'newkailipingjuzhishu':newkailipingjuzhishu,
                    'newkailikeshengzhishu':newkailikeshengzhishu,
                    'peifulv':peifulv,
                }
                rangqiuModel.save(rangqiu)

    def parsePeilv(self, response):
        data = response.xpath("//div[@class='clearfix container_wrapper pankoudata']")
        matchModel = MatchModel()
        companyModel = CompanyModel()
        peilvModel = PeilvModel()
        for i in data:
            matchName = i.xpath("div//p//b/text()")[0].extract()
            matchTime = i.xpath("div//p//b")[2].extract()
            matchTime = etree.HTML(matchTime).xpath("//b/text()")
            year = None
            if matchTime[0][:5] == response.meta['yd'][-5:]:
                year = response.meta['yd'][:4]
            elif matchTime[0][:5] == response.meta['rc1'][-5:]:
                year = response.meta['rc1'][:4]
            elif matchTime[0][:5] == response.meta['rc2'][-5:]:
                year = response.meta['rc2'][:4]
            elif matchTime[0][:5] == response.meta['rc3'][-5:]:
                year = response.meta['rc3'][:4]
            else:
                continue
            matchTime = year + '-' + matchTime[0] + ':00'
            if self.get_week_day(datetime.datetime.strptime(matchTime[0:10], '%Y-%m-%d')) == matchName[0:2]:
                matchKey = matchTime[:4] + matchTime[5:7] + matchTime[8:10] + matchName[-3:]
                pass
            else:
                ## 判断前两天是否满足
                g = -2
                mingzhongdate = None
                while g < 2:
                    tmpdate = datetime.datetime.strptime(matchTime[0:10], '%Y-%m-%d')
                    tmpdate = (tmpdate + g * Day())
                    if self.get_week_day(tmpdate) ==  matchName[0:2]:
                        mingzhongdate = tmpdate
                        break
                    g = g + 1
                if mingzhongdate == None:
                    continue
                else:
                    mingzhongdate = datetime.datetime.strftime(mingzhongdate, "%Y%m%d")
                    matchKey = mingzhongdate + matchName[-3:]
            match = matchModel.getMatchIdByKey(matchKey)
            if match == None:
                continue
            
            list = i.xpath("table//tr")

            e = 0
            for item in list:
                e = e + 1
                if e < 3:
                    continue
                itemData = item.xpath("td").extract()
                if len(itemData) == 5:
                    continue
                v1 = itemData[0]
                v5 = itemData[5]
                v6 = itemData[6]
                v7 = itemData[7]
                company = etree.HTML(v1).xpath("//td//span/text()")[0]
                company = companyModel.getCompanyIdByName(company)
                if len(etree.HTML(v5).xpath("//td//a//span/text()")) == 0:
                    continue
                zz = self.myFloat(etree.HTML(v5).xpath("//td//a//span/text()")[0])
                pz = self.myFloat(etree.HTML(v6).xpath("//td//a//span/text()")[0])
                kz = self.myFloat(etree.HTML(v7).xpath("//td//a//span/text()")[0])
                peilv = {
                    'match':match,
                    'company':company,
                    'zz':zz,
                    'pz':pz,
                    'kz':kz
                }
                peilvModel.save(peilv)

    def get_week_day(self, date):
        day = date.weekday()
        return self.week_day_dict[day]