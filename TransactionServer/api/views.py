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

@logRequest
@api_view(['GET'])
def quote(request, **kwargs):
    userId = "621c2225545c6aa5b6b9b83a"
    # TODO: redis this, then have the buy and sell commands use the redis cache before hitting the quote server
    ticker = kwargs.get('ticker')
    if ticker is None:
        ticker = request.GET.get('ticker')
    if ticker is None:
        raise Exception('No ticker specified')
    try:
        if ticker is None:
            raise Exception("ticker not specified")
        return Response(getQuote(ticker, userId,request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
    
@logRequest
@api_view(['POST', 'PATCH'])
def add(request):
     
    
    userId = "621c2225545c6aa5b6b9b83a"
    amount = request.data.get('amount', False) 
    try:
        return Response(addBalance(userId, amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
                 
@logRequest
@api_view(['POST'])
def buy(request):
    userid = "621c2225545c6aa5b6b9b83a"
    ticker = request.data.get('ticker', False)
    amount = request.data.get('amount', False)
    try: 
        return Response(buyStock(userid, amount,getQuote(ticker,userid, request.transactionId), request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@logRequest
@api_view(['PATCH'])
def commit_buy(request):
    
    userid = "621c2225545c6aa5b6b9b83a"
    try:
        return Response(commitBuy(userid, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
         

@logRequest
@api_view(['POST'])
def cancel_buy(request): 
    userid = "621c2225545c6aa5b6b9b83a"
    try:
        return Response(cancelBuy(userid, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@logRequest
@api_view(['POST'])
def sell(request):
    userid = "621c2225545c6aa5b6b9b83a"
    amount = request.data.get('amount', False)
    ticker = request.data.get('ticker', False)
    try:
        return Response(sellStock(userid, amount, getQuote(ticker, userid, request.transactionId), request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@logRequest
@api_view(['POST'])
def commit_sell(request):
    userid = "621c2225545c6aa5b6b9b83a"
    try:
        return Response(commitSell(userid, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@logRequest
@api_view(['POST'])
def cancel_sell(request):
    userid = "621c2225545c6aa5b6b9b83a"
    try:
        return Response(cancelSell(userid, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@logRequest
@api_view(['POST'])
def set_buy_amount(request): 
    userid = "621c2225545c6aa5b6b9b83a"
    amount = request.data.get('amount', False)
    ticker = request.data.get('ticker', False)
    try:
        return Response(setBuyAmount(userid, ticker,amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@logRequest
@api_view(['POST'])
def cancel_set_buy(request):
    userid = "621c2225545c6aa5b6b9b83a"
    ticker = request.data.get('ticker', False)
    try:
        return Response(cancelBuyTrigger(userid,ticker,request.transactionId))
    except Exception as e:
        return handleViewError(e, request)

@logRequest
@api_view(['POST'])
def set_buy_trigger(request):
    userid = "621c2225545c6aa5b6b9b83a"
    ticker = request.data.get('ticker', False)
    price = request.data.get('price', False)
    try:
        return Response(setBuyTrigger(userid, ticker, price,request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@logRequest
@api_view(['POST'])
def set_sell_amount(request):
    userid = "621c2225545c6aa5b6b9b83a"
    amount = request.data.get('amount', False)
    try:
        return Response(setSellAmount(userid, amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@logRequest
@api_view(['POST'])
def set_sell_trigger(request):
    userid = "621c2225545c6aa5b6b9b83a"
    price = request.data.get('price', False)
    ticker = request.data.get('ticker', False)
    try:
        return Response(setSellTrigger(userid, ticker, price, request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@logRequest
@api_view(['POST'])
def cancel_set_sell(request):
    userid = "621c2225545c6aa5b6b9b83a"
    ticker = request.data.get('ticker', False)
    try:
        return Response(cancelSellTrigger(userid, ticker,request.transactionId))
    except Exception as e:
        return handleViewError(e, request)
@logRequest
@api_view(['GET'])
def dumplog(request):
    try:
        if 'userid' in request.GET.keys():
            return Response(dumplogXML(request.GET['userid']))
        return Response(dumplogXML())
    except Exception as e:
        return handleViewError(e, request)
    

@logRequest
@api_view(['GET'])
def displaySummary(request):  
    return Response("not implemented")
    

@csrf_exempt
@api_view(['POST'])
def createNewUser(request):
    try:
        body = request.data

        if(createUser(body['name'], body['email'], body['password'])):
            # TODO: log the user in when the account is created
            return Response("User created")
        
    except Exception as e:
        
        return handleViewError(e, request)

@api_view(['GET'])
def getUserObj(request):
    try:
        user = getUser("621c2225545c6aa5b6b9b83a")
        print(user)
        return Response(user)
    except Exception as e:
        return handleViewError(e, request)

