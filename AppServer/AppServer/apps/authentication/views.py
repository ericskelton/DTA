from functools import partial
from pickle import TRUE
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from .models import User
import requests


from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, AddSerializer
)

class UserAddAmountToBalanceAPIView(RetrieveUpdateAPIView):
    permission_clases = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = AddSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        print("ADD UPDATE REQUEST DATA:  ", request.data)
        print("ADD UPDATE REQUEST USER: ", request.user)
        print('ADD UPDATE REQUEST ADD', request.add)
        serializer = self.serializer_class(request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        

        user = request.data.get('user',{})
        print("views patch for add amount. request data ", request.data)
        #it will verify that this user exists
        
        serializer = self.serializer_class(user,
            data=request.data, partial=True)
        print("views patch for s")
        serializer.is_valid(raise_exception=True)
        print("here. serializer is ", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

        #will be routed to mongo server

class QuoteRetrieveAPIView(RetrieveAPIView):
    #permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
        username = request.GET.get('username', '')
        if username is None:
            return Response("username is required", status=status.HTTP_400_BAD_REQUEST)
        ticker = request.GET.get('ticker', '')
        message = "transaction server endpoint: quote "
        params = {"message": message, "username": username, "ticker": ticker}
        return Response(params, status=status.HTTP_200_OK)
        # TO DO
        transaction_server_response = requests.get(TRAANSACTION_SERVER + 'quote', params=params)

        return Response(transaction_server_response, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
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