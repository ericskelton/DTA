import sys
import requests

def main():

    with open(sys.argv[1]) as f: #Reading in the file
        lines = f.readlines() 

    userID = 0
    lines_formatted = [] 

    for i in range(len(lines)): #String formatting and appending to larger list
        without_line_breaks = lines[i].replace("\n","")
        separate_by_comma = without_line_breaks.split(",")
    
        lines_formatted.append(separate_by_comma)

    for element in range(len(lines_formatted)): #Finding all commands and sending them to their correct function
        lines_formatted[element][0] = lines_formatted[element][0].split(" ")
        if ("ADD" == lines_formatted[element][0][1]):

            add(lines_formatted[element][1], lines_formatted[element][2])

        if ("QUOTE" == lines_formatted[element][0][1]):

            quote(lines_formatted[element][1], lines_formatted[element][2])

        if ("BUY" == lines_formatted[element][0][1]):

            buy(lines_formatted[element][1],lines_formatted[element][2],lines_formatted[element][3])

        if ("COMMIT_BUY" == lines_formatted[element][0][1]):

            commit_buy(lines_formatted[element][1])

        if ("CANCEL_BUY" == lines_formatted[element][0][1]):

            cancel_buy(lines_formatted[element][1])

        if ("SELL" == lines_formatted[element][0][1]):

            sell(lines_formatted[element][1],lines_formatted[element][2],lines_formatted[element][3])

        if ("COMMIT_SELL" == lines_formatted[element][0][1]):

            commit_sell(lines_formatted[element][1])

        if ("CANCEL_SELL" == lines_formatted[element][0][1]):

            cancel_sell(lines_formatted[element][1])

        if ("SET_BUY_AMOUNT" == lines_formatted[element][0][1]):

            set_buy_amount(lines_formatted[element][1],lines_formatted[element][2],lines_formatted[element][3])

        if ("CANCEL_SET_BUY" == lines_formatted[element][0][1]):

            cancel_set_buy(lines_formatted[element][1],lines_formatted[element][2])

        if ("SET_BUY_TRIGGER" == lines_formatted[element][0][1]):

            set_buy_trigger(lines_formatted[element][1],lines_formatted[element][2],lines_formatted[element][3])

        if ("SET_SELL_AMOUNT" == lines_formatted[element][0][1]):

            set_sell_amount(lines_formatted[element][1],lines_formatted[element][2],lines_formatted[element][3])

        if ("SET_SELL_TRIGGER" == lines_formatted[element][0][1]):

            set_sell_trigger(lines_formatted[element][1],lines_formatted[element][2],lines_formatted[element][3])

        if ("CANCEL_SET_SELL" == lines_formatted[element][0][1]):

            cancel_set_sell(lines_formatted[element][1],lines_formatted[element][2])

        if ("DUMPLOG" == lines_formatted[element][0][1]):

            dumplog(lines_formatted[element][1])

        if ("DISPLAY_SUMMARY" == lines_formatted[element][0][1]):

            display_summary(lines_formatted[element][1])            
            
# ADD Function - All functionality related to adding funds to a user's account

def add(userid, amount):

    endpoint = "API-URL/add"
    payload = {"user_id" : userid, "amount" : amount}

    r = requests.post(url=endpoint, data=payload)

def quote(userid, symbol):

    endpoint = "API-URL/quote"
    parameters = {"symbol": symbol}    

    r = requests.get(url = endpoint, params=parameters)

def buy(userid, symbol, amount):

    endpoint = "API-URL/buy"
    payload = {"user_id" : userid, "symbol" : symbol, "amount" : amount}

    r = requests.post(url=endpoint, data=payload)
    
def commit_buy(userid):

    endpoint = "API-URL/commit-buy"
    payload = {"user_id" : userid}

    r = requests.post(url=endpoint, data=payload)

def cancel_buy(userid):

    endpoint = "API-URL/cancel-buy"
    payload = {"user_id" : userid}

    r = requests.post(url=endpoint, data=payload)

def sell(userid, symbol, amount):

    endpoint = "API-URL/sell"
    payload = {"user_id" : userid, "symbol" : symbol, "amount" : amount}

    r = requests.post(url=endpoint, data=payload)

def commit_sell(userid):

    endpoint = "API-URL/commit-sell"
    payload = {"user_id" : userid}

    r = requests.post(url=endpoint, data=payload)

def cancel_sell(userid):

    endpoint = "API-URL/cancel-sell"
    payload = {"user_id" : userid}

    r = requests.post(url=endpoint, data=payload)

def set_buy_amount(userid,symbol,amount):

    endpoint = "API-URL/set-buy-amount"
    payload = {"user_id" : userid, "symbol" : symbol, "amount" : amount}

    r = requests.post(url=endpoint, data=payload)

def cancel_set_buy(userid, symbol):

    endpoint = "API-URL/cancel-set-buy"
    payload = {"user_id" : userid, "symbol" : symbol}

    r = requests.post(url=endpoint, data=payload)

def set_buy_trigger(userid,symbol,amount):

    endpoint = "API-URL/set-buy-trigger"
    payload = {"user_id" : userid, "symbol" : symbol, "amount" : amount}

    r = requests.post(url=endpoint, data=payload)

def set_sell_amount(userid,symbol,amount):

    endpoint = "API-URL/set-sell-amount"
    payload = {"user_id" : userid, "symbol" : symbol, "amount" : amount}

    r = requests.post(url=endpoint, data=payload)

def set_sell_trigger(userid,symbol,amount):

    endpoint = "API-URL/set-sell-trigger"
    payload = {"user_id" : userid, "symbol" : symbol, "amount" : amount}

    r = requests.post(url=endpoint, data=payload)

def cancel_set_sell(userid, symbol):

    endpoint = "API-URL/cancel-set-sell"
    payload = {"user_id" : userid, "symbol" : symbol}

    r = requests.post(url=endpoint, data=payload)

def dumplog(filename):

    endpoint = "API-URL/dumplog"  

    r = requests.get(url = endpoint)

    f = open(filename,"w+")
    f.write(r)

def display_summary(userid):

    endpoint = "API-URL/display-summary"
    r = requests.get(url = endpoint, params=userid)

    



if __name__ == '__main__':
    main()
