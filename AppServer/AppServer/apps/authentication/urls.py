from django.urls import path


from .views import (
    LoginAPIView,
    QuoteRetrieveAPIView, 
    RegistrationAPIView, 
    UserRetrieveUpdateAPIView,
    UserAddAmountToBalanceAPIView
    )

app_name = 'authentication'
urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('add', UserAddAmountToBalanceAPIView.as_view()),
    path('quote', QuoteRetrieveAPIView.as_view())
]