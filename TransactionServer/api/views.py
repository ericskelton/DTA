from sys import stdout
from django.shortcuts import render
from django.http import HttpResponse
from api.utils.quoteServer import getQuote
from api.utils.user import *
from api.utils.errors import handleViewError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
from api.utils.log import logRequest

@logRequest
@api_view(['GET'])
def quote (request):
    # TODO: redis this, then have the buy and sell commands use the redis cache before hitting the quote server
    return Response(getQuote(request.GET['ticker']))
    
@logRequest
@api_view(['POST', 'PATCH'])
def add(request):
     
    body = request.POST
    # TODO: userId needs to be real (authenticated and shit)
    userId = "6211857dc98b9aa98bf047a9"
    amount = body['amount']
    return Response(addBalance(userId, amount, request.transactionId))
                 
@logRequest
@api_view(['POST'])
def buy(request):
    
    userid = "6211857dc98b9aa98bf047a9"
    return Response(buyStock(userid, request.POST['amount'], request.transactionId))

@logRequest
@api_view(['POST'])
def commit_buy(request):
    userid = "6211857dc98b9aa98bf047a9"
    return Response(commitBuy(userid, request.transactionId))

@logRequest
@api_view(['POST'])
def cancel_buy(request): 
    userid = "6211857dc98b9aa98bf047a9"
    return Response(cancelBuy(userid, request.transactionId))

@logRequest
@api_view(['POST'])
def sell(request):
    userid = "6211857dc98b9aa98bf047a9"
    return Response(sellStock(userid, request.POST['amount'], request.transactionId))

@logRequest
@api_view(['POST'])
def commit_sell(request):
    userid = "6211857dc98b9aa98bf047a9"
    return Response(commitSell(userid, request.transactionId))

@logRequest
@api_view(['POST'])
def cancel_sell(request):
    userid = "6211857dc98b9aa98bf047a9"
    return Response(cancelSell(userid, request.transactionId))

@logRequest
@api_view(['POST'])
def set_buy_amount(request): 
    userid = "6211857dc98b9aa98bf047a9"
    return Response(setBuyAmount(userid, request.POST['amount'], request.transactionId))

@logRequest
@api_view(['POST'])
def cancel_set_buy(request):
    pass

@logRequest
@api_view(['POST'])
def set_buy_trigger(request):
    userid = "6211857dc98b9aa98bf047a9"
    return Response(setBuyTrigger(userid, request.POST['trigger']))

@logRequest
@api_view(['POST'])
def set_sell_amount(request):
    return Response("Not implemented")

@logRequest
@api_view(['POST'])
def set_sell_trigger(request):
    Response("Not implemented")
    
@logRequest
@api_view(['POST'])
def cancel_set_sell(request):
    return Response("Not implemented")
    
@logRequest
@api_view(['GET'])
def dumplog(request):
    if 'userid' in request.GET.keys():
        return Response(dumplogXML(request.GET['userid']))
    return Response(dumplogXML())
    

@logRequest
@api_view(['GET'])
def displaySummary(request):  
    return Response("not implemented")
    

@csrf_exempt
@api_view(['POST'])
def createNewUser(request):
    try:
        body = request.POST

        if(createUser(body['name'], body['email'], body['password'])):
            # TODO: log the user in when the account is created
            return Response("User created")
        
    except Exception as e:
        
        return handleViewError(e, request)

@api_view(['GET'])
def getUserObj(request):
    try:
        user = getUser("6211857dc98b9aa98bf047a9")
        print(user)
        return Response(user)
    except Exception as e:
        return handleViewError(e, request)

