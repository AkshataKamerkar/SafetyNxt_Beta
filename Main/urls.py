from django.urls import path
from .views import LandingPage, AboutUs

app_name = 'main'

urlpatterns = [
    path('',LandingPage.as_view(),name='index'),
    path('/about',AboutUs.as_view(),name='about'),
]