import sys
import argparse

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
            add(userID, lines_formatted[element][2])
        if ("QUOTE" == lines_formatted[element][0][1]):
            quote()
        if ("BUY" == lines_formatted[element][0][1]):
            buy()
        if ("COMMIT_BUY" == lines_formatted[element][0][1]):
            commit_buy()
        if ("CANCEL_BUY" == lines_formatted[element][0][1]):
            cancel_buy()
        if ("SELL" == lines_formatted[element][0][1]):
            sell()
        if ("COMMIT_SELL" == lines_formatted[element][0][1]):
            commit_sell()
        if ("CANCEL_SELL" == lines_formatted[element][0][1]):
            cancel_sell()
        if ("SET_BUY_AMOUNT" == lines_formatted[element][0][1]):
            set_buy_amount()
        if ("CANCEL_SET_BUY" == lines_formatted[element][0][1]):
            cancel_set_buy()
        if ("SET_BUY_TRIGGER" == lines_formatted[element][0][1]):
            set_buy_trigger()
        if ("SET_SELL_AMOUNT" == lines_formatted[element][0][1]):
            set_sell_amount()
        if ("SET_SELL_TRIGGER" == lines_formatted[element][0][1]):
            set_sell_trigger()
        if ("CANCEL_SET_SELL" == lines_formatted[element][0][1]):
            cancel_set_sell()
        if ("DUMPLOG" == lines_formatted[element][0][1]):
            dumplog()
        if ("DISPLAY_SUMMARY" == lines_formatted[element][0][1]):
            display_summary()            
            
# ADD Function - All functionality related to adding funds to a user's account

def add(userid, amount):

    print("ADD DETECTED")

# QUOTE Function - 

def quote():

    print("QUOTE DETECTED")

def buy():

    print("BUY DETECTED")

def commit_buy():

    print("COMMIT BUY DETECTED")

def cancel_buy():

    print("CANCEL BUY DETECTED")

def sell():

    print("SELL DETECTED")

def commit_sell():

    print("COMMIT SELL")

def cancel_sell():

    print("CANCEL SELL DETECTED")

def set_buy_amount():

    print("SET BUY DETECTED")

def cancel_sell():

    print("CANCEL SELL DETECTED")

def cancel_set_buy():

    print("CANCEL SET BUY DETECTED")

def set_buy_trigger():

    print("SET BUY TRIGGER DETECTED")

def set_sell_amount():

    print("SET SELL DETECTED")

def set_sell_trigger():

    print("SET SELL TRIGGER DETECTED")

def cancel_set_sell():

    print("CANCEL SET SELL DETECTED")

def dumplog():

    print("DUMPLOG DETECTED")

def display_summary():

    print("DISPLAY SUMMARY DETECTED")




if __name__ == '__main__':
    main()
