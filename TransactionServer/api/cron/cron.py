from api.utils.user import getTriggers, buyStock, sellStock, commitBuy, commitSell
from api.utils.quoteServer import getQuote
from api.utils.db import logJsonObject
import time
def trigger_job():
    triggers = getTriggers()
    transactionId = logJsonObject({'type': 'systemEvent', 'event': 'trigger_job', 'server': 'transactionserver', 'timestamp': str(int(time.time()))})
    startTime = time.time()
    triggers_executed = 0
    for stock in triggers:
        quote = getQuote(stock)
        if triggers[stock]['type'] == 'buy' and quote['price'] <= triggers[stock]['price']: 
            buyStock(triggers[stock]['userid'], triggers[stock]['amount'], transactionId)
            commitBuy(triggers[stock]['userid'], stock, transactionId)
            triggers_executed += 1
        elif triggers[stock]['type'] == 'sell' and quote['price'] >= triggers[stock]['price']: 
            sellStock(sell_triggers[stock]['userid'], sell_triggers[stock]['amount'], transactionId)
            commitSell(sell_triggers[stock]['userid'], stock, transactionId)
            triggers_executed += 1
            

    logJsonObject({'type': 'systemevent', 'event': 'trigger_job_executed', 'activeTriggers': str(len(buy_triggers.keys()) + len(sell_triggers.keys())), 'triggers_executed': triggers_executed, 'time': str(time.time() - startTime) + ' seconds', 'transactionId': transactionId})

    return


if __name__ == '__main__':
    trigger_job()