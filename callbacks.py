from hashlib import new
from weakref import ref
from dash import Output,Input,MATCH,State,ctx,dcc
import pandas as pd
import yfinance as yf
from app import app
from datetime import date
from functions import *
import plotly.graph_objects as go

today = date.today()
# dd/mm/YY day month year
dmy = today.strftime("%d/%m/%Y")

app.callback(
    Output({'type':'stock-input','index':'CAD'},'valid'),
    Output({'type':'stock-input','index':'CAD'},'invalid'),
    Input({'type':'stock-input','index':'CAD'},'value')
)(checkvalid)

#Adds to stocks to Table

@app.callback(
    Output({'type':'datatable','index':MATCH},'data'),
    Output({'type':'datatable','index':MATCH},'tooltip_data'),
    Input({'type':'stock-confirm','index':MATCH},'n_clicks'),
    Input({'type':'interval','index':MATCH},'n_intervals'),
    State({'type':'datatable','index':MATCH},'data'),
    State({'type':'datatable','index':MATCH},'tooltip_data'),
    State({'type':'stock-input','index':MATCH},'value'),
    State({'type':'amount-input','index':MATCH},'value'),
    State({'type':'price-input','index':MATCH},'value'),
    prevent_initial_call=True
)

def addToTable(clicks,intervals,data,tooltips,ticker,amount,price):
    inputMethod = ctx.triggered_id
    if 'stock-confirm' in inputMethod['type']:
        market = inputMethod['index']
        rowdict = {}
        indata = False
        Cachelist =[]

        for row in data:
            if ticker == row['Ticker']: #METHOD WORKS
                indata = True
                oldamount = int(row['# of Shares'])
                oldprice = float(row['Average Cost'])

                newprice = (oldprice*oldamount + amount*price) / (amount + oldamount)
                newprice = round(newprice,2)

                newamount = int(amount + oldamount)

                row['# of Shares'] = newamount
                row['Average Cost'] = newprice

                #needs to cache new value

                Cachelist.append([market,'date',row['Ticker'],newamount,newprice])
            else:
                print('no')

        df = pd.DataFrame(data)

        #if ticker in dataframe
        # change amount and price
        #else
        
        #df.loc[ticker]
        if indata == False:
            data, longsummary = grabStockInfo(market,ticker,price,amount)
            for i in range(len(data)):
                rowdict[df.columns[i]]=data[i]

            df2 = pd.DataFrame(rowdict,columns=df.columns,index=[0])
            outdf = pd.concat([df,df2],ignore_index=True)

            currenttip = {df.columns[0]:longsummary}
            tooltips.append(currenttip)

            cacheStocks(market,dmy,ticker,price,amount)

            return outdf.to_dict('records'),tooltips
        
        file = open('Cache/Current.txt','w')
        for stocklist in Cachelist:
            file.write(str(stocklist)) #needs to be fixed to regular format
        file.close()

        return df.to_dict('records'),tooltips
        # print('1')
        # fixedstockname  = ticker + '.TO'
        # stock = yf.Ticker(fixedstockname)
        # print('2')

        # outname,sector,industry,longsummary,marketprice,open,divyield,yeardiv= stock.info['longName'],stock.info['sector'],stock.info['industry'],stock.info['longBusinessSummary'],stock.info['currentPrice'],stock.info['open'],stock.info['dividendYield'],stock.info['dividendRate']
        
        # #print(stock.info)
        # #daychange uses yesterdays close
        # daychange = (marketprice - open)/open * 100
        # gain = (marketprice-price) * amount
        # gainpercent = gain/(price * amount) * 100
        # total = marketprice * amount
        # try:
        #     yeardiv = float(yeardiv)
        #     divyield = float(divyield)
        # except:
        #     yeardiv = 0
        #     divyield = 0
        # totaldiv = amount * float(yeardiv)
        # divyield = divyield * 100

        # data = [outname,ticker,sector,industry,amount,round(price,2),round(marketprice,2),round(daychange,2),yeardiv,round(divyield,2),totaldiv,round(gainpercent,2),round(gain,2),round(total,2),'p/e']

        
    else:
        print('refreshing')

        market = inputMethod['index']
        try:
            refreshStock(market,data)
        except:
            pass

        #Interval Method
        #for stock in data:
        #print(data)
        """ removefirst = False
        for stock in data:
            if stock['Stock Name'] == 0:
                if len(data) > 1:
                    removefirst = True
                    #data.remove(stock)
            else:
                for column in stock:
                    test = refreshStock(stock)
                    currentstock = stock['Ticker']
                    currentstock = currentstock + '.TO'
                    current = yf.Ticker(currentstock)
                    marketprice,open,divyield,yeardiv= current.info['currentPrice'],current.info['open'],current.info['dividendYield'],current.info['dividendRate']

                    daychange = (marketprice - open)/open * 100
                    gain = (marketprice-price) * amount
                    gainpercent = gain/(price * amount) * 100
                    total = marketprice * amount

                    # 'Market Price','Day Change %','Dividend/Share','Dividend Yield','Dividend','Gain %','Gain','Total Equity','P/E'
                    # round(marketprice,2),round(daychange,2),yeardiv,divyield,totaldiv,round(gainpercent,2),round(gain,2),round(total,2),'p/e'

                    if column == 'Market Price':
                        stock[column] = round(marketprice,2)
                    elif column == 'Day Change %':
                        stock[column] = round(daychange,2)
                    elif column == 'Gain %':
                        stock[column] = round(gainpercent,2)
                    elif column == 'Gain':
                        stock[column] = round(gain,2)
                    elif column == 'Total Equity':
                        stock[column] = round(total,2)
                    elif column == 'P/E':
                        stock[column] = 'new p/e'

        if removefirst == True:
            data.remove(data[0])

        print('end refresh')
        print(data) """
        #Does end refresh but new isnt good

        return data,tooltips

#Makes graph based on selected datatable rows

@app.callback(
    Output({'type':'graph-container','index':MATCH},'children'),
    Input({'type':'datatable','index':MATCH},'selected_rows'),
    Input({'type':'graph-radios','index':MATCH},'value'),
    State({'type':'datatable','index':MATCH},'data')
)
def graphDataTable(rows,value,alldata):
    #where rows is a list of lists
    inputMethod = ctx.triggered_id
    if rows != None:
        selectedrows = []

        #print(rows)
        #print('value',value)

        # should really just grab tickers
        # for row in rows:
        #     selectedrows.append(alldata[row])

        for row in rows:
            ticker = alldata[row]['Ticker']
            if inputMethod['index'] == 'CAD':
                ticker = ticker + '.TO'
            selectedrows.append(ticker)

        tickerstring = ' '.join(selectedrows)

        #print(tickerstring)

        if value == 1:
            period = '1d'
            interval = '30m'
        elif value == 2:
            period = '5d'
            interval = '90m'
        elif value == 3:
            period = '1mo'
            interval = '1d'
        elif value == 4:
            period = '3mo'
            interval = '1d'
        elif value == 5:
            period = 'ytd'
            interval = '1wk'

        data = yf.download(tickerstring,period = period,interval = interval,group_by = 'ticker')
        #has Datetime, Open, High, Low, Close, Adj Close, Volume
        #print('data',data)
        #print(data['BCE.TO'].columns())

        fig = go.Figure()

        #if more than 1 selected
        for tick in selectedrows:
            tickdata = data[tick]
            fig.add_trace(
                go.Scatter(
                    x=tickdata.index, 
                    y=tickdata['Close'],
                    mode='lines+markers',
                    name='lines+markers'
                )
            )

        newchild = dcc.Graph(figure=fig)
        #print('selected rows',selectedrows)
        #newchild = px.line
        return newchild
    else:
        return None