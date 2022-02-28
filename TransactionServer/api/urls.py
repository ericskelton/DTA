from django.urls import path
from . import views

urlpatterns = [
    path('quote/<str:ticker>/', views.quote, name='quote'),
    path('quote/', views.quote, name='quote'),
    path('add/', views.add, name='add'),
    path('createUser/', views.createNewUser, name='createUser'), # don't need to log this one
    path('getUser/',  views.getUserObj, name='getUser'),
    path('getUser/<str:userId>/', views.getUserObj, name='getUser'),
    path('buy/', views.buy, name='buy'),
    path('commitBuy/', views.commit_buy, name='commit_buy'),
    path('cancelBuy/', views.cancel_buy, name='cancel_buy'),
    path('sell/', views.sell, name='sell'),
    path('cancelSell/', views.cancel_sell, name='cancel_sell'),
    path('commitSell/', views.commit_sell, name='commit_sell'),
    path('setBuyTrigger/', views.set_buy_trigger, name='set_buy_trigger'),
    path('setSellAmount/', views.set_sell_amount, name='set_sell_amount'),
    path('setSellTrigger/', views.set_sell_trigger, name='set_sell_trigger'),
    path('dumplog/', views.dumplog, name='dumplog'),
    path('displaySummary/', views.displaySummary, name='displaySummary'),
]