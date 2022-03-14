from api.utils.user import getTriggers, buyStock, sellStock, commitBuy, commitSell
from api.utils.quoteServer import getQuote
from api.utils.db import logJsonObject, dbCallWrapper, getDb
import time
import pymongo

db, client = getDb()

def trigger_job():
    triggers = getTriggers()
    transactionNum = db.log.find_one({'type': 'userCommand'}, {'transactionNum': 1}, sort=[('_id', pymongo.DESCENDING)])
    startTime = int(time.time() * 1000)  
    transactionNum = transactionNum['transactionNum'] + 1 if 'transactionNum' in transactionNum.keys() else 1
    logJsonObject({'type': 'systemEvent', 'event': 'trigger_job', 'server': 'transactionserver', 'timestamp': startTime, 'transactionNum': transactionNum})
    transactionId = transactionNum
    triggers_executed = 0
    for trigger in triggers:
        for stock in trigger['buy_triggers'].keys():
            quote = getQuote(stock, trigger['_id'], transactionId)
            if trigger['buy_triggers'][stock]['price'] > quote['price']:
                buyStock(trigger['_id'], trigger['buy_triggers'][stock]['amount'], quote, transactionId)
                commitBuy(trigger['_id'], transactionId)

                # remove trigger

                dbCallWrapper({}, {'$set': {'buy_triggers.' + stock: None}}, func=db.user.update_one)

                triggers_executed += 1
        for stock in trigger['sell_triggers'].keys():
            quote = getQuote(stock, trigger['_id'], transactionId)
            if trigger['sell_triggers'][stock]['price'] < quote['price']:
                sellStock(trigger['_id'], trigger['sell_triggers'][stock]['amount'], quote, transactionId)
                commitSell(trigger['_id'], transactionId)
                dbCallWrapper({}, {'$set': {'sell_triggers.' + stock: None}}, func=db.user.update_one)
                triggers_executed += 1
            

    logJsonObject({'type': 'systemevent', 'event': 'trigger_job_executed',  'triggers_executed': triggers_executed, 'time': str(time.time() - startTime) + ' milliseconds', 'transactionId': transactionId})

    return


if __name__ == '__main__':
    trigger_job()