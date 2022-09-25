import ast
import yfinance as yf

def tickersTor():
    CADEXCH = ['TSX','TSXV']
    outputlist=[]
    for exch in CADEXCH:
        finame = 'Data/' + exch + '.txt'
        file = open(finame,'r')
        for line in file:
            splitline = line.split('\t')
            outputlist.append(splitline[0])
    return outputlist

def readData(filename):
    file = open(filename,'r')
    output = file.read()
    file.close()
    return output

def writeData(filename,lines):
    file = open(filename,'w')
    file.write(lines)
    file.close()

def cacheStocks(market,date,stock,price,amount):
    file = open('Cache/Current.txt','a')
    outputlist = [market,date,stock,price,amount]
    file.write(str(outputlist) + '\n')
    file.close()

def checkStockCache(market):
    file = open('Cache/Current.txt','r')
    outputlines = file.readlines()
    file.close()

    output = []

    for line in outputlines:
        listline = ast.literal_eval(line)
        if listline[0] == market:
            output.append(listline)
    return output

def checkvalid(value):
    CADTickers = tickersTor()
    if value != None and value != '':
        # try:
        #     data = yf.download(tickers=value,period='30m',interval='1h')
        #     return True,False
        # except Exception as EGC:
        #     print(EGC)
        #     return False,True
        if value in CADTickers:
            return True,False
        else:
            return False,True
    else:
        return False,False

def grabStockInfo(market,ticker,price,amount):
    if market == 'CAD' and ticker[-3:] != '.TO':
        fixedstockname = ticker + '.TO'

    stock = yf.Ticker(fixedstockname)

    #print(stock.info.keys)
    #['Stock Name','Ticker','Sector','Industry','# of Shares','Average Cost','Market Price','Day Change %','Dividend/Share','Dividend Yield','Dividend','Gain %','Gain','Total Equity','P/E']
    # maybe use 'trailingEps'

    #TOTAL LIST OF .info methods
    # (['zip', 'sector', 'fullTimeEmployees', 'longBusinessSummary', 'city', 'state', 'country', 'companyOfficers', 'website', 'maxAge', 'address1', 'industry', 'address2', 'ebitdaMargins', 'profitMargins',
    # 'grossMargins', 'operatingCashflow', 'revenueGrowth', 'operatingMargins', 'ebitda', 'targetLowPrice', 'recommendationKey', 'grossProfits', 'freeCashflow', 'targetMedianPrice', 'currentPrice', 
    # 'earningsGrowth', 'currentRatio', 'returnOnAssets', 'numberOfAnalystOpinions', 'targetMeanPrice', 'debtToEquity', 'returnOnEquity', 'targetHighPrice', 'totalCash', 'totalDebt', 'totalRevenue', 
    # 'totalCashPerShare', 'financialCurrency', 'revenuePerShare', 'quickRatio', 'recommendationMean', 'exchange', 'shortName', 'longName', 'exchangeTimezoneName', 'exchangeTimezoneShortName', 'isEsgPopulated', 
    # 'gmtOffSetMilliseconds', 'quoteType', 'symbol', 'messageBoardId', 'market', 'annualHoldingsTurnover', 'enterpriseToRevenue', 'beta3Year', 'enterpriseToEbitda', '52WeekChange', 'morningStarRiskRating', 'forwardEps',
    # 'revenueQuarterlyGrowth', 'sharesOutstanding', 'fundInceptionDate', 'annualReportExpenseRatio', 'totalAssets', 'bookValue', 'sharesShort', 'sharesPercentSharesOut', 'fundFamily', 'lastFiscalYearEnd', 'heldPercentInstitutions', 
    # 'netIncomeToCommon', 'trailingEps', 'lastDividendValue', 'SandP52WeekChange', 'priceToBook', 'heldPercentInsiders', 'nextFiscalYearEnd', 'yield', 'mostRecentQuarter', 'shortRatio', 'sharesShortPreviousMonthDate', 'floatShares', 'beta',
    # 'enterpriseValue', 'priceHint', 'threeYearAverageReturn', 'lastSplitDate', 'lastSplitFactor', 'legalType', 'lastDividendDate', 'morningStarOverallRating', 'earningsQuarterlyGrowth', 'priceToSalesTrailing12Months', 
    # 'dateShortInterest', 'pegRatio', 'ytdReturn', 'forwardPE', 'lastCapGain', 'shortPercentOfFloat', 'sharesShortPriorMonth', 'impliedSharesOutstanding', 'category', 'fiveYearAverageReturn', 'previousClose', 'regularMarketOpen',
    # 'twoHundredDayAverage', 'trailingAnnualDividendYield', 'payoutRatio', 'volume24Hr', 'regularMarketDayHigh', 'navPrice', 'averageDailyVolume10Day', 'regularMarketPreviousClose', 'fiftyDayAverage', 'trailingAnnualDividendRate',
    # 'open', 'toCurrency', 'averageVolume10days', 'expireDate', 'algorithm', 'dividendRate', 'exDividendDate', 'circulatingSupply', 'startDate', 'regularMarketDayLow', 'currency', 'trailingPE', 'regularMarketVolume', 'lastMarket',
    # 'maxSupply', 'openInterest', 'marketCap', 'volumeAllCurrencies', 'strikePrice', 'averageVolume', 'dayLow', 'ask', 'askSize', 'volume', 'fiftyTwoWeekHigh', 'fromCurrency', 'fiveYearAvgDividendYield', 'fiftyTwoWeekLow', 'bid',
    # 'tradeable', 'dividendYield', 'bidSize', 'dayHigh', 'coinMarketCapLink', 'regularMarketPrice', 'preMarketPrice', 'logo_url', 'trailingPegRatio'])

    outname,sector,industry,longsummary,marketprice,open,divyield,yeardiv,prevclose = stock.info['longName'],stock.info['sector'],stock.info['industry'],stock.info['longBusinessSummary'],stock.info['currentPrice'],stock.info['open'],stock.info['dividendYield'],stock.info['dividendRate'],stock.info['previousClose']

    #print(stock.info)
    #daychange uses yesterdays close
    daychange = (marketprice - prevclose)/prevclose * 100
    gain = (marketprice-price) * amount
    gainpercent = gain/(price * amount) * 100
    total = marketprice * amount
    try:
        yeardiv = float(yeardiv)
        divyield = float(divyield)
    except:
        yeardiv = 0
        divyield = 0
    totaldiv = amount * float(yeardiv)
    divyield = divyield * 100

    data = [outname,ticker,sector,industry,amount,round(price,2),round(marketprice,2),round(daychange,2),yeardiv,round(divyield,2),totaldiv,round(gainpercent,2),round(gain,2),round(total,2),'p/e']
    return data,longsummary

def refreshStock(market,entiredata):
    #works okay but it still needs to me better
    tickerlist = []

    for stock in entiredata:
        currentstock = stock['Ticker']
        if currentstock == 0:
            pass
        else:
            tickerlist.append(stock['Ticker'] + '.TO')

    batchcommand = ' '.join(tickerlist)

    tickers = yf.Tickers(batchcommand)
    outputdata =[]
    amount = 1
    price = 1

    print(tickers.tickers)
    for each in tickerlist:
        entireinfo = tickers.tickers[each].info
        outname,sector,industry,longsummary,marketprice,open,divyield,yeardiv,prevclose = entireinfo['longName'],entireinfo['sector'],entireinfo['industry'],entireinfo['longBusinessSummary'],entireinfo['currentPrice'],entireinfo['open'],entireinfo['dividendYield'],entireinfo['dividendRate'],entireinfo['previousClose']

        daychange = (marketprice - prevclose)/prevclose * 100
        gain = (marketprice-price) * amount
        gainpercent = gain/(price * amount) * 100
        total = marketprice * amount
        try:
            yeardiv = float(yeardiv)
            divyield = float(divyield)
        except:
            yeardiv = 0
            divyield = 0
        totaldiv = amount * float(yeardiv)
        divyield = divyield * 100

        outputdata.append([outname,each,sector,industry,amount,round(price,2),round(marketprice,2),round(daychange,2),yeardiv,round(divyield,2),totaldiv,round(gainpercent,2),round(gain,2),round(total,2),'p/e'])

    print(outputdata)
    #How Data comes in
    #{'Stock Name': 'BCE Inc.', 'Ticker': 'BCE', 'Sector': 'Communication Services', 'Industry': 'Telecom Services', '# of Shares': 100, 'Average Cost': 60, 'Market Price': 63.71, 'Day Change %': 1.22, 'Dividend/Share': 3.68, 'Dividend Yield': 5.69, 'Dividend': 368, 'Gain %': 6.18, 'Gain': 371, 'Total Equity': 6371, 'P/E': 'p/e'}
    
    #cycle through all data first grabbing tickers then batch call then output repectively
    #Each interval should be for one table since Match command

    # print(stockdict)
    # return stockdict

#refreshStock('CAD',[{'Ticker':'BCE'},{'Ticker':'TD'}])

# data = yf.download('BCE.TO BB.TO',period = '1d',interval = '30m',group_by = 'ticker')
# bell = data['BCE.TO']

# # print(bell)
# print(bell.index)
#.index for datetime, close for closing