from email import message
from functools import partial
from logging import raiseExceptions
from pickle import TRUE
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from .models import User
import requests
from .permissions.permissions import DumplogPermissions
import json

from .serializers import (
    LoginSerializer, 
    RegistrationSerializer, 
    UserSerializer,  
    UsernameAmountStockSerializer, 
    UsernameSerializer,
    UsernameStockSerializer,
    UsernameDumplogSerializer,
    UsernameAmountSerializer,
    DumplogSerializer

)



        #will be routed to mongo server

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        print("data being passed to serializer is, ", user)

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)



    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
       

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, 
            data=serializer_data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class AddAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user, partial=True)
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/add/', params=serializer.data)

        message = {"message": "add amount endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class QuoteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameStockSerializer

    def get(self, request):
        params = request.query_params
        serializer = self.serializer_class(data=params)
        serializer.is_valid(raise_exception=True)
        r = requests.get('https://dta-transaction-server.herokuapp.com/api/quote/', params=serializer.data)
        message = {"message": "quote endpoint", "serializer_data": serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class BuyStockAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(
            data=user
        
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post(url='https://dta-transaction-server.herokuapp.com/api/buy/',  data=serializer.data)
        message = {"message": "buy stock endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class CommitBuyAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(
            data=user
        
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/commit_buy/', data=serializer.data)
        message = {"message": "commit buy endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class CancelBuyAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(
            data=user, 
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/cancel_buy/', data=serializer.data)
        message = {"message": "cancel buy endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class SellStockAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(

            data=user

        )
        
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/sell/', data=serializer.data)
        message = {"message": "sell stock endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class CommitSellAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/commit_sell/', data=serializer.data)
        message = {"message": "commit sell endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class CancelSellAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(
            data=user
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/cancel_sell/', data=serializer.data)
        message = {"message": "cancel sell endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class SetBuyAmountAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class( 
            data=user
            
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/set_buy_amount/', data=serializer.data)
        
        message = {"message": "set buy amount endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class CancelSetBuyAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(
            data=user
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/cancel_set_buy/', data=serializer.data)
        
        message = {"message": "cancel set buy endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class SetBuyTriggerAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class( 
            data=user
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/set_buy_trigger/', data=serializer.data)
        
        message = {"message": "set buy trigger endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class SetSellAmountAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(
            data=user
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/set_sell_amount/', data=serializer.data)
        
        message = {"message": "set sell amount endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class SetSellTriggerAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(
            data=user, 
        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/set_sell_trigger/', data=serializer.data)
        
        message = {"message": "set sell trigger endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class CancelSetSellAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(

            data=user

        )
        serializer.is_valid(raise_exception=True)
        r = requests.post('https://dta-transaction-server.herokuapp.com/api/cancel_set_sell/', data=serializer.data)
        
        message = {"message": "set sell trigger endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

#get probably
class DumpLogAPIVeiw(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameDumplogSerializer

    def get(self, request):
        params = request.query_params
        serializer = self.serializer_class(data=params)
        serializer.is_valid(raise_exception=True)
        r = requests.get('https://dta-transaction-server.herokuapp.com/api/dumplog/', params=serializer.data)
        message = {"message": "dunmplog endpoint", "serializer_data": serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)

class DumpLogAdminAPIVeiw(APIView):
    permission_classes = (IsAdminUser,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = DumplogSerializer

    def get(self, request):
        params = request.query_params
        serializer = self.serializer_class(data=params)
        serializer.is_valid(raise_exception=True)
        r = requests.get(url='https://dta-transaction-server.herokuapp.com/api/dumplog/', params=serializer.data)
        message = {"message": "dunmplog endpoint", "serializer_data": serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)
    
class DisplaySummary(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer
    
    def get(self, request):
        user = request.query_params
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        r = requests.get(url='https://dta-transaction-server.herokuapp.com/api/display_summary/', params=serializer.data)
        message = {"message": "set sell trigger endpoint", "serializer_data":serializer.data, "response from transaction": r.text}
        return Response(message, status=status.HTTP_200_OK)