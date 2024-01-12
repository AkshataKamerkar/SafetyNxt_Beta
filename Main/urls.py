from django.urls import path
from .views import LandingPage, AboutUs, GetLLs, LogInSignUp, Main

app_name = 'main'

urlpatterns = [
    path('',LandingPage.as_view(),name='index'),
    path('about',AboutUs.as_view(),name='about'),
    path('info',GetLLs.as_view(),name='info'),
    path('log',LogInSignUp.as_view(),name='log'),
    path('menu',Main.as_view(),name='menu'),
]