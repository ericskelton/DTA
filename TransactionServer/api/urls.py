from django.urls import path
from . import views

# we need to log each call to the api
# so we are just going to wrap the views in a logger

urlpatterns = [
    path('quote/', views.quote, name='quote'),
    path('add/', views.add, name='add'),
    path('createUser/', views.createNewUser, name='createUser'), # don't need to log this one
    path('getUser/',  views.getUserObj, name='getUser'),
    path('getUser/<str:userId>/', views.getUserObj, name='getUser'),
    path('buy/', views.buy, name='buy'),
    path('commitBuy/', views.commitBuy, name='commitBuy'),
    path('cancelBuy/', views.cancelBuy, name='cancelBuy'),
    path('sell/', views.sell, name='sell'),
    path('cancelSell/', views.cancelSell, name='cancelSell'),
    path('commitSell/', views.commitSell, name='commitSell'),
    path('setBuyTrigger/', views.setBuyTrigger, name='setBuyTrigger'),
    path('setSellAmount/', views.setSellAmount, name='setSellAmount'),
    path('setSellTrigger/', views.setSellTrigger, name='setSellTrigger'),
    path('dumplog/', views.dumplog, name='dumplog'),
    path('displaySummary/', views.displaySummary, name='displaySummary'),
]