from django.urls import path
from .views import LandingPage, AboutUs, GetLLs

app_name = 'main'

urlpatterns = [
    path('',LandingPage.as_view(),name='index'),
    path('/about',AboutUs.as_view(),name='about'),
    path('/info',GetLLs.as_view(),name='info'),
]