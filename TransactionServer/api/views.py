from django.shortcuts import render
from django.http import HttpResponse
from api.utils.quoteServer import getQuote
from api.utils.user import *



# Create your views here.

def quote (request):
    if(request.method == 'GET'):
        return HttpResponse(getQuote(request.GET['ticker']))
    else:
        return HttpResponse("Invalid request")

def add(request):
    if(request.method == 'POST'):
        body = request.POST
        # TODO: userId needs to be real (authenticated and shit)
        userId = body['user']
        amount = body['amount']
        return HttpResponse(addBalance(userId, amount))
        

                 
    else:
        return HttpResponse("Invalid request")
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

def createNewUser(request):
    if(request.method == 'POST'):
        body = request.POST

        if(createUser(body['name'], body['email'], body['password'])):
            return HttpResponse("User created")
        else:
            return HttpResponse("User already exists")
    else:
        return HttpResponse("Invalid request")

        