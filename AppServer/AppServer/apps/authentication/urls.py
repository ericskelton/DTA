from django.urls import path


from .views import (
    LoginAPIView,
    QuoteAPIView, 
    RegistrationAPIView, 
    UserRetrieveUpdateAPIView,
    AddAPIView,
    QuoteAPIView,
    BuyStockAPIView,
    CommitBuyAPIView,
    CancelBuyAPIView,
    SellStockAPIView,
    CommitSellAPIView,
    CancelSellAPIView,
    SetBuyAmountAPIView,
    CancelSetBuyAPIView,
    SetBuyTriggerAPIView,
    SetSellAmountAPIView,
    SetSellTriggerAPIView,
    CancelSellSetAPIView,
    DumpLogAPIVeiw,
    DisplaySummary,
    DumpLogAdminAPIVeiw
    )

app_name = 'authentication'
urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    #DTA specific
    path('add/', AddAPIView.as_view()),
    path('quote', QuoteAPIView.as_view()),
    path('buy', BuyStockAPIView.as_view()),
    path('commitbuy/', CommitBuyAPIView.as_view()),
    path('cancelbuy/', CancelBuyAPIView.as_view()),
    path('sell/', SellStockAPIView.as_view()),
    path('commitsell/', CommitSellAPIView.as_view()),
    path('cancelsell/', CancelSellAPIView.as_view()),
    path('setbuyamount/', SetBuyAmountAPIView.as_view()),
    path('cancelsetbuy/', CancelSetBuyAPIView.as_view()),
    path('setbuytrigger/', SetBuyTriggerAPIView.as_view()),
    path('setsellamount/', SetSellAmountAPIView.as_view()),
    path('setselltrigger/', SetSellTriggerAPIView.as_view()),
    path('cancelsetsell/', CancelSellSetAPIView.as_view()),
    path('dumplog', DumpLogAPIVeiw.as_view()),
    path('displaysummary', DisplaySummary.as_view()),
    path('dumpnlogadmin', DumpLogAdminAPIVeiw.as_view()),

]