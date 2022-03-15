from api.utils.user import getTriggers, buyStock, sellStock, commitBuy, commitSell, getUser
from api.utils.quoteServer import getQuote
from api.utils.db import logJsonObject, dbCallWrapper, getDb
import time
from bson.objectid import ObjectId

db, client = getDb()

def trigger_job():
    triggers = getTriggers()
    
    startTime = int(time.time() * 1000)  
    
    
    
    triggers_executed = 0
    for trigger in triggers:
        for stock in trigger['buy_triggers'].keys():
            if not trigger['buy_triggers'][stock]:
                continue
            user = getUser(trigger['buy_triggers'][stock]['userid'])
            quote = getQuote(stock, user, 'not used anymore')
            if trigger['buy_triggers'][stock] and trigger['buy_triggers'][stock]['price'] > quote['price']:
                objId = logJsonObject({'type': 'systemEvent', 'filename': 'trigger_job', 'server': 'transactionserver', 'timestamp': int(time.time() * 1000), 'stockSymbol': stock, 'username': trigger['buy_triggers'][stock]['userid']})
                
                transactionId = str(int(ObjectId(objId).binary.hex(), 16))
                try:
                    user = getUser(trigger['buy_triggers'][stock]['userid'])
                    buyStock(user, trigger['buy_triggers'][stock]['amount'], quote, transactionId)
                    commitBuy(user, transactionId)
                except:
                    pass

                # remove trigger
                dbCallWrapper({}, {'$set': {'buy_triggers.' + stock: None}}, func=db.user.update_one)

                triggers_executed += 1
        for stock in trigger['sell_triggers'].keys():
            if not trigger['sell_triggers'][stock]:
                continue
            user = getUser(trigger['sell_triggers'][stock]['userid'])
            quote = getQuote(stock, user, 'not used anymore')
            if trigger['sell_triggers'][stock] and trigger['sell_triggers'][stock]['price'] < quote['price']:
                objId = logJsonObject({'type': 'systemEvent', 'filename': 'trigger_job', 'server': 'transactionserver', 'timestamp': int(time.time() * 1000), 'stockSymbol': stock, 'username': trigger['buy_triggers'][stock]['userid']})
                
                transactionId = str(int(ObjectId(objId).binary.hex(), 16))
                
                try:
                    
                    sellStock(user, trigger['sell_triggers'][stock]['amount'], quote, transactionId)
                    commitSell(user, transactionId)
                except:
                    pass
                dbCallWrapper({}, {'$set': {'sell_triggers.' + stock: None}}, func=db.user.update_one)
                triggers_executed += 1
            

    

    return


if __name__ == '__main__':
    trigger_job()