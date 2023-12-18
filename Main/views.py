from django.shortcuts import render
from django.views.generic import TemplateView, FormView


# Creating the Landing Page
class LandingPage(TemplateView):

    template_name = 'landingPage.html'

# Creating the About Us Page
class AboutUs(TemplateView):

    template_name = 'about.html'

class LogInSignUp(FormView):

    template_name = 'log.html'


class GetLLs(FormView):

    template_name = 'getInfo.html'