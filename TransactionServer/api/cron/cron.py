from api.utils.user import getTriggers, buyStock, sellStock, commitBuy, commitSell
from utils.quoteServer import getQuote
from api.utils.db import logJsonObject
import time
def trigger_job():
    triggers = getTriggers()
    sell_triggers = triggers['sell_triggers']
    buy_triggers = triggers['buy_triggers']
    transactionId = logJsonObject({'type': 'systemEvent', 'event': 'trigger_job', 'server': 'transactionserver', 'timestamp': str(int(time.time()))})
    startTime = time.time()
    triggers_executed = 0
    for stock in buy_triggers:
        quote = getQuote(stock)
        if quote['price'] <= buy_triggers[stock]['price']:
            buyStock(buy_triggers[stock]['userid'], buy_triggers[stock]['amount'], transactionId)
            commitBuy(buy_triggers[stock]['userid'], stock, transactionId)
            triggers_executed += 1
    for stock in sell_triggers:
        quote = getQuote(stock)
        if quote['price'] >= sell_triggers[stock]['price']:
            sellStock(sell_triggers[stock]['userid'], sell_triggers[stock]['amount'], transactionId)
            commitSell(sell_triggers[stock]['userid'], stock, transactionId)
            triggers_executed += 1

    logJsonObject({'type': 'systemevent', 'event': 'trigger_job_executed', 'activeTriggers': str(len(buy_triggers.keys()) + len(sell_triggers.keys())), 'triggers_executed': triggers_executed, 'time': str(time.time() - startTime) + ' seconds', 'transactionId': transactionId})

    return


if __name__ == '__main__':
    trigger_job()