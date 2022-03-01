from django.urls import path
from . import views

urlpatterns = [
    path('quote/<str:ticker>/', views.quote, name='quote'),
    path('quote/', views.quote, name='quote'),
    path('add/', views.add, name='add'),
    path('create_user/', views.createNewUser, name='createUser'), # don't need to log this one
    path('get_user/',  views.getUserObj, name='getUser'),
    path('get_user/<str:userId>/', views.getUserObj, name='getUser'),
    path('buy/', views.buy, name='buy'),
    path('commit_buy/', views.commit_buy, name='commit_buy'),
    path('cancel_buy/', views.cancel_buy, name='cancel_buy'),
    path('sell/', views.sell, name='sell'),
    path('cancel_sell/', views.cancel_sell, name='cancel_sell'),
    path('commit_sell/', views.commit_sell, name='commit_sell'),
    path('set_buy_trigger/', views.set_buy_trigger, name='set_buy_trigger'),
    path('set_buy_amount/', views.set_buy_amount, name='set_buy_amount'),
    path('set_sell_amount/', views.set_sell_amount, name='set_sell_amount'),
    path('set_sell_trigger/', views.set_sell_trigger, name='set_sell_trigger'),
    path('cancel_set_buy/', views.cancel_set_buy, name='cancel_set_buy'),
    path('cancel_set_sell/', views.cancel_set_sell, name='cancel_set_sell'),
    path('dumplog/', views.dumplog, name='dumplog'),
    path('display_summary/', views.displaySummary, name='displaySummary'),
]