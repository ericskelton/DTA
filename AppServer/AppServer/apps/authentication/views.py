from email import message
from functools import partial
from logging import raiseExceptions
from pickle import TRUE
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from .models import User
import requests
from .permissions.permissions import DumplogPermissions

from .serializers import (
    LoginSerializer, 
    RegistrationSerializer, 
    UserSerializer,  
    UsernameAmountStockSerializer, 
    UsernameSerializer,
    UsernameStockSerializer,
    UsernameDumplogSerializer
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
        print("in api view for request data is ", request.data)
        print("request user is: ", request.user)
        print("retrieve user api view serializer_data is: ", serializer_data)
        print("about to go into user serializer update function")
        serializer = self.serializer_class(
            request.user, 
            data=serializer_data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class AddAPIView(RetrieveUpdateAPIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user, partial=True)
        serializer.is_valid(raise_exception=True)
        message = {"message": "add amount endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class QuoteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameStockSerializer

    def retrieve(self, request):
        params = request.query_params
        serializer = self.serializer_class(params)
        serializer.is_valid(raise_exception=True)
        message = {"message": "quote endpoint", "serializer_data": serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class BuyStockAPIView(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user, partial=True)
        serializer.is_valid(raise_exception=True)
        message = {"message": "buy stock endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class CommitBuyAPIView(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "commit buy endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class CancelBuyAPIView(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "cancel buy endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class SellStockAPIView(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "sell stock endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class CommitSellAPIView(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "commit sell endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class CancelSellAPIView(RetrieveAPIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "cancel sell endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class SetBuyAmountAPIView(RetrieveAPIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "set buy amount endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class CancelSetBuyAPIView(RetrieveAPIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "cancel set buy endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class SetBuyTriggerAPIView(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "set buy trigger endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class SetSellAmountAPIView(RetrieveAPIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "set sell amount endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class SetSellTriggerAPIView(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameAmountStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "set sell trigger endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class CancelSellSetAPIView(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameStockSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "set sell trigger endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

#get probably
class DumpLogAPIVeiw(APIView):
    permission_clases = (DumplogPermissions,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameDumplogSerializer

    def retrieve(self, request):
        params = request.query_params
        serializer = self.serializer_class(params)
        serializer.is_valid(raise_exception=True)
        message = {"message": "dunmplog endpoint", "serializer_data": serializer.data}
        return Response(message, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "dump log for admin", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)

class DisplaySummary(APIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsernameSerializer
    
    def retreive(self, request):
        user = request.data.query_params
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        message = {"message": "set sell trigger endpoint", "serializer_data":serializer.data}
        return Response(message, status=status.HTTP_200_OK)