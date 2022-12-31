from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from os.path import exists

import requests
import json
import calendar
import os
import time

class Binance:
    URL = "https://www.binance.com/bapi/margin/v1/public/margin/vip/spec/history-interest-rate?asset=%%coin%%&vipLevel=0&size=90&startTime=%%startTime%%&endTime=%%endTime%%"
    DEBUGFILE = "debug/log.txt"
    DISTDIR = "dist/"
    # COINS    = ["AGLD","MATIC","STPT","APT","STG","IOTX","SHIB","TVK","FRONT","GLM","KDA","RAY","NEAR","AUDIO","HNT","DOCK","STX","FARM","PNT","DENT","QI","AION","NPXS","MBOX","DGB","ZRX","SANTOS","WING","WNXM","IOST","BCH","BSW","CAKE","OMG","JST","BAND","HOT","SUN","ASTR","GMT","BTC","RSR","TWT","NKN","AR","IOTA","CVC","IRIS","REEF","GMX","BTG","RAMP","MIR","LOKA","CVP","KEY","BTS","COVER","BTT","CVX","FLM","ONE","GNO","ONG","ANKR","SUSHI","VITE","ALGO","SC","ONT","CFX","T","SFP","DIA","BTTC","ACA","FIRO","ARDR","MANA","NEBL","ACH","BEL","MINA","VTHO","ATA","NMR","MKR","DODO","LIT","WOO","ICP","REI","ZEC","REN","REP","ADA","ELF","ICX","REQ","STORJ","POLYX","BZRX","LOOM","DF","ZEN","RARE","PAXG","KP3R","DOGE","DUSK","ALPHA","HBAR","SXP","RVN","CHR","MLN","AUD","NANO","WAVES","CHZ","ADX","XRP","CTSI","JASMY","FIDA","KAVA","SAND","C98","OSMO","OCEAN","FOR","UMA","VIDT","AVA","SYS","COCOS","STRAX","GAL","SCRT","TUSD","GAS","TKO","RGT","THETA","ENJ","YFII","WAN","GRT","HARD","NEXO","TFUEL","ORN","PERL","ENS","LEND","MASK","TROY","AAVE","UNI","TLM","GBP","PERP","CKB","BOND","WRX","LUNC","YFI","LUNA","XTZ","GMXUSDT","MOB","EOS","BICO","SKL","GTC","XEC","YGG","PEOPLE","AXS","ZIL","BURGER","XEM","CTXC","GTO","WTC","XVG","EPS","BIDR","DNT","CLV","EPX","FLOW","COMP","XVS","SLP","OOKI","RUNE","NBS","GMXBUSD","FORTH","KMD","GHST","LEVER","LAZIO","DOT","IQ","IDEX","1INCH","CHESS","DEXE","AVAX","MITH","DEGO","UNFI","FTM","POWR","ERN","KNC","PROS","PROM","VOXEL","FTT","PHA","RLC","PHB","ATOM","QUICK","BLZ","HIVE","LPT","SNM","BIFI","MBL","SNX","FUN","PORTO","COS","API3","PYR","ROSE","WAXP","GLMR","DAI","SOL","DAR","FET","ETC","BNB","OGN","CELR","UST","ETH","NEO","CELO","KLAY","TOMO","AUCTION","LRC","BADGER","XZC","HIGH","GXS","MTL","VET","TRB","ALPACA","USDT","BNT","OXT","DASH","BNX","UTK","ILV","HEGIC","AMB","MC","TRU","DREP","TRX","BTCST","MDT","MDX","JOE","AERGO","EUR","AMP","LSK","KEEP","NULS","USTC","BEAM","AUTO","DCR","CREAM","DATA","IMX","ANC","EGLD","LTC","USDC","WIN","PUNDIX","SPELL","FXS","INJ","PLA","TCT","CRV","LTO","VGX","ANT","BAKE","NU","TRIBE","DYDX","FLUX","ANY","SRM","POND","TORN","LINA","LDO","QNT","MAGIC","ALICE","XLM","OG","LINK","MFT","QTUM","OM","OP","SUPER","POLS","KSM","FIL","BQX","POLY","STMX","RNDR","FIO","BAL","GALA","VIB","BETA","FIS","RAD","BAT","APE","AKRO","MOVR","BUSD","CTK","ARPA","XMR","COTI","ALCX"]
    COINS = ["BTC"]

    def __init__(self, startYear, startMonth, endYear, endMonth):
        self.startYear = startYear
        self.startMonth = startMonth
        self.endYear = endYear
        self.endMonth = endMonth
        self.startTime = self.getDateTimeObj(startYear, startMonth, True)
        self.endTime = self.getDateTimeObj(endYear, endMonth, False)

    def doRequest(self, coin, startTime, endTime):
        response = requests.get(self.getRequestUrl(coin, startTime, endTime))
        if (response.status_code == 200):
            try:
                reJson = response.json()
            except:
                self.writeLog(f"Fail to attempt json object, {coin}, {startTime}, {endTime}")
                return

            dirName = self.DISTDIR + coin + "/"
            if not exists(dirName):
                os.mkdir(dirName)

            distFilePath = dirName + startTime.strftime("%Y-%b") + ".json"  # dir name, dist/{coin}/{month}.json
            self.writeFile(distFilePath, reJson, exists(distFilePath))

        else:
            self.writeLog(f"Fail with status code {response.status_code}, {coin}, {startTime}, {endTime}")

        time.sleep(1)
        return

    def execute(self):
        for coin in self.COINS:
            self.retrieve(coin, self.startTime, self.endTime)

    def getDateTimeObj(self, year, month, isStart):
        day = 1 if isStart else calendar.monthrange(year, month)[1]
        return datetime(year, month, day)

    def getRequestUrl(self, coin, startTime, endTime):
        return self.URL.replace("%%coin%%", coin)\
            .replace("%%startTime%%", str(int(startTime.timestamp() * 1000)))\
            .replace("%%endTime%%", str(int(endTime.timestamp() * 1000)))

    def retrieve(self, coin, start_time, end_time):
        dateRange = relativedelta(end_time, start_time)
        if dateRange.months < 1 and dateRange.years == 0:
            print(f"date range <= 1 month, {coin}, {start_time}, {end_time}")
            self.doRequest(coin, start_time, end_time)
        else:
            thisMonth = start_time + relativedelta(months=+1, days=-1)
            print(f"date range > 1 month, {coin}, {start_time}, {end_time}, get this month {thisMonth}")
            self.doRequest(coin, start_time, thisMonth)

            nextMonth = start_time + relativedelta(months=+1)
            self.retrieve(coin, nextMonth, end_time)
        return True

    def writeFile(self, distFilePath, reJson, isExists):
        if not reJson['data']:
            self.writeLog(f"data is empty, {distFilePath}")
            return

        coinFile = open(distFilePath, ("r+" if isExists else "w+"))
        jsonCoinFile = json.load(coinFile) if isExists else []
        for data in reJson['data']:
            jsonCoinFile.append(data)

        if isExists: coinFile.seek(0)

        coinFile.write(json.dumps(jsonCoinFile))
        coinFile.close()

    def writeLog(self, logMsg):
        logFile = open(self.DEBUGFILE, "a+")
        logFile.write(logMsg + "\n")
        logFile.close()


binance = Binance(startYear=2022, startMonth=10, endYear=2022, endMonth=12)
binance.execute()