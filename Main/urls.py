from django.urls import path
from .views import LandingPage, AboutUs, Map
from . import views

app_name = 'main'

urlpatterns = [
    path('',LandingPage.as_view(),name='index'),
    path('about',AboutUs.as_view(),name='about'),
    path('menu',Map.as_view(),name='menu'),
    path('coordinates/',views.get_coordinates,name='coordinates')
]