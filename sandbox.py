from ib_insync import *
# util.startLoop() # uncomment this line when in a notebook
import pandas as pd
from calculating_allocation import tickerDict

ib = IB()
ib.connect(host='127.0.0.1', port=7496, clientId=1)
account = 'DU2440468'

# set the account we're connecting to
acc = ib.accountSummary(account=account)

# variable that holds the value of the portfolio
portVal = 0

for i in acc:
    if i[1] == 'NetLiquidation':
        # set the net liquidation value of portfolio as portfolio value
        portVal = float(i[2])

print('Net Liquidation value of portfolio is {}'.format(portVal))

for key, value in tickerDict.items():
    print(key, value[0], value[1])

allocationDict = {}

for ticker in tickerDict:
    purchaseValue = int(tickerDict[ticker][1] * portVal)
    numShares = int(purchaseValue / tickerDict[ticker][0])

    allocationDict.update({ticker: numShares})

    print('We are purchasing ${} of {}, which translates into {} shares'
          .format(purchaseValue, ticker, numShares))


def check_for_duplicate_orders(ticker):
    # need to call this before ib.OpenTrades() will provide us with the open order information we need from
    # ib.openTrades()

    orderID_list = []

    openTrades = ib.openTrades()

    # look through each trade in the openTrades list
    for i in range(len(openTrades)):
        print(openTrades[i])

        # if there is an open trade with the same ticker as the trade we are trying to enter
        if openTrades[i].contract.symbol == ticker:

            # print(openTrades[i])
            print(openTrades[i].orderStatus.orderId)
            orderID_list.append(openTrades[i].orderStatus.orderId)

            # need to access the openOrders object because it has the orderID attribute
            # which is required in ib.cancelOrder
            openOrders = ib.openOrders()

            # if there is an item in openOrders with the same orderId in orderID_list
            # cancel that order
            for z in range(len(openOrders)):
                if openOrders[z].orderId in orderID_list:
                    ib.cancelOrder(openOrders[z])


currentPositions = ib.positions(account=account)
positionDict = {}

for i in currentPositions:
    positionDict.update({i.contract.symbol: i.position})

tradeDict = {}

for ticker in allocationDict:

    print(ticker)

    if ticker in positionDict:

        if allocationDict[ticker] > positionDict[ticker]:

            tradeAmount = allocationDict[ticker] - positionDict[ticker]
            tradeAction = 'BUY'

        else:
            tradeAmount = positionDict[ticker] - allocationDict[ticker]
            tradeAction = 'SELL'

    else:
        tradeAmount = allocationDict[ticker]
        tradeAction = 'BUY'

    tradeDict.update({ticker: (tradeAction, tradeAmount)})

print(tradeDict)

for key, value in tradeDict.items():

    check_for_duplicate_orders(key)

    ib.placeOrder(contract=Stock(symbol=key, exchange='SMART', currency='USD'),
                  order=MarketOrder(action=value[0], totalQuantity=value[1]))


