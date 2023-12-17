from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

# Creating the Landing Page
class LandingPage(TemplateView):

    template_name = 'landingPage.html'

# Creating the About Us Page
class AboutUs(TemplateView):

    template_name = 'about.html'

