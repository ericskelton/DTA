from api.utils.user import getTriggers, buyStock, sellStock, commitBuy, commitSell
from api.utils.quoteServer import getQuote
from api.utils.db import logJsonObject
import time
def trigger_job():
    triggers = getTriggers()
    transactionId = logJsonObject({'type': 'systemEvent', 'event': 'trigger_job', 'server': 'transactionserver', 'timestamp': str(int(time.time()))})
    startTime = time.time()
    triggers_executed = 0
    for trigger in triggers:
        
        for stock in trigger['buy_triggers'].keys():
            quote = getQuote(stock, trigger['_id'], transactionId)
            if trigger['buy_triggers'][stock]['price'] > quote[stock]:
                buyStock(trigger['_id'], trigger['buy_triggers'][stock]['amount'], quote, transactionId)
                commitBuy(trigger['_id'], transactionId)
                triggers_executed += 1
        for stock in trigger['sell_triggers'].keys():
            quote = getQuote(stock, trigger['_id'], transactionId)
            if trigger['sell_triggers'][stock]['price'] < quote[stock]:
                sellStock(trigger['_id'], trigger['sell_triggers'][stock]['amount'], quote, transactionId)
                commitSell(trigger['_id'], transactionId)
                triggers_executed += 1
    endTime = time.time()
            

    logJsonObject({'type': 'systemevent', 'event': 'trigger_job_executed',  'triggers_executed': triggers_executed, 'time': str(time.time() - startTime) + ' seconds', 'transactionId': transactionId})

    return


if __name__ == '__main__':
    trigger_job()