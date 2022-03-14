from sys import stdout
from django.shortcuts import render
from django.http import HttpResponse
from api.utils.quoteServer import getQuote
from api.utils.user import *
from api.utils.errors import handleViewError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.utils.log import logRequest
import json 

@logRequest
@api_view(['GET'])
def quote(request, **kwargs):
    username = "test"
    # TODO: redis this, then have the buy and sell commands use the redis cache before hitting the quote server
    ticker = kwargs.get('ticker')
    if ticker is None:
        ticker = request.GET.get('ticker')
    try:
        if ticker is None:
            raise Exception('No ticker specified')
    
        
        return Response(getQuote(ticker, username,request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@csrf_exempt
@logRequest
@api_view(['POST', 'PATCH'])
def add(request):
     
    
    username = request.data.get('username')
    print(username)
    amount = request.data.get('amount', False) 
    print(amount)
    print(request.data)
    try:
        return Response(addBalance(username, amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@csrf_exempt               
@logRequest
@api_view(['POST'])
def buy(request):
    username = request.data.get('username')
    ticker = request.data.get('ticker', False)
    amount = request.data.get('amount', False)
    try: 
        if ticker == False: 
            raise Exception('No ticker specified')
        if amount == False:
            raise Exception('No amount specified')
    
        return Response(buyStock(username, amount,getQuote(ticker,username, request.transactionId), request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@csrf_exempt
@logRequest
@api_view(['POST','PATCH'])
def commit_buy(request):
    
    username = request.data.get('username')
    try:
        return Response(commitBuy(username, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
         

@csrf_exempt
@logRequest
@api_view(['POST'])
def cancel_buy(request): 
    username = request.data.get('username')
    try:
        return Response(cancelBuy(username, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@csrf_exempt
@logRequest
@api_view(['POST'])
def sell(request):
    username = request.data.get('username')
    amount = request.data.get('amount', False)
    ticker = request.data.get('ticker', False)
    try:
        return Response(sellStock(username, amount, getQuote(ticker, username, request.transactionId), request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@csrf_exempt
@logRequest
@api_view(['POST'])
def commit_sell(request):
    username = request.data.get('username')
    try:
        return Response(commitSell(username, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@csrf_exempt
@logRequest
@api_view(['POST'])
def cancel_sell(request):
    username = request.data.get('username')
    try:
        return Response(cancelSell(username, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@csrf_exempt
@logRequest
@api_view(['POST'])
def set_buy_amount(request): 
    username = request.data.get('username')
    amount = request.data.get('amount', False)
    ticker = request.data.get('ticker', False)
    try:
        return Response(setBuyAmount(username, ticker,amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@csrf_exempt
@logRequest
@api_view(['POST'])
def cancel_set_buy(request):
    username = request.data.get('username')
    ticker = request.data.get('ticker', False)
    try:
        return Response(cancelBuyTrigger(username,ticker,request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@csrf_exempt
@logRequest
@api_view(['POST'])
def set_buy_trigger(request):
    username = request.data.get('username')
    ticker = request.data.get('ticker', False)
    price = request.data.get('price', False)
    try:
        return Response(setBuyTrigger(username, ticker, price,request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@csrf_exempt
@logRequest
@api_view(['POST'])
def set_sell_amount(request):
    username = request.data.get('username')
    amount = request.data.get('amount', False)
    ticker = request.data.get('ticker', False)
    try:
        return Response(setSellAmount(username, ticker, amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@csrf_exempt
@logRequest
@api_view(['POST'])
def set_sell_trigger(request):
    username =  request.data.get('username')
    price = request.data.get('price', False)
    ticker = request.data.get('ticker', False)
    try:
        return Response(setSellTrigger(username, ticker, price, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@csrf_exempt
@logRequest
@api_view(['POST'])
def cancel_set_sell(request):
    username = request.data.get('username')
    ticker = request.data.get('ticker', False)
    try:
        return Response(cancelSellTrigger(username, ticker,request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@logRequest
@api_view(['GET'])
def dumplog(request):
    try:
        if 'username' in request.GET.keys():
            return Response(dumplogXML(request.GET['username']))
        return Response(dumplogXML())
    except Exception as e:
        return handleViewError(e, request)
    

@logRequest
@api_view(['GET'])
def displaySummary(request):  
    try:
        username = request.GET.get('username')
        return Response(displayUserSummary(username))
    except Exception as e:
        return handleViewError(e, request)
    

@csrf_exempt
@api_view(['POST'])
def createNewUser(request):
    try:
        body = request.data

        if(createUser(body['name'], body['username'], body['password'])):
            # TODO: log the user in when the account is created
            return Response("User created")
        
    except Exception as e:
        
        return handleViewError(e, request)

@api_view(['GET'])
def getUserObj(request):
    try:

        user = getUser("test")
        print(user)
        return Response(user)
    except Exception as e:
        return handleViewError(e, request)

