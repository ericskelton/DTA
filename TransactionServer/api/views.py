from django.shortcuts import render
from django.http import HttpResponse
from api.utils.quoteServer import quoteServer

# Create your views here.

def quote (request):
    if(request.method == 'GET'):
        print(request.GET['ticker'])
        return HttpResponse(quoteServer.getQuote(request.GET['ticker']))
    else:
        return HttpResponse("Invalid request")

def add(request):
    pass
def buy(request):
    pass
def commit_buy(request):
    pass
def cancel_buy(request):
    pass
def sell(request):
    pass
def commit_sell(request):
    pass
def cancel_sell(request):
    pass
def set_buy_amount(request):
    pass
def cancel_set_buy(request):
    pass
def set_buy_trigger(request):
    pass
def set_sell_amount(request):
    pass
def set_sell_trigger(request):
    pass
def cancel_set_sell(request):
    pass
def dumplog(request):
    pass
def display_summary(request):  
    pass