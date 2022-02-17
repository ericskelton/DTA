from django.shortcuts import render
from .serializers import UserSerializer, SnippetSerializer, CustomUserSerializer
from .models import Snippet
from django.contrib.auth.models import User
from .models import CustomUser
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework import viewsets

# def

# class ADDViewSet(viewsets.ViewSet):
#     serializer_class = ADDSerializer

#     def

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

@api_view(['PATCH'])  
def add(request, *args, **kwargs):
    try:
        
        print("here: ", request.data["id"])
        
        user_id = request.data["id"]
        user = CustomUser.objects.get(id=user_id)
        #WIP for authentication
        # if not user.is_authenticated():
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    new_amount = request.data["amount"]
    user.balance = user.balance + new_amount
    user.save()
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)
    # if serializer.is_valid():
    #         print("not valid")
    #         serializer.save()
            
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)