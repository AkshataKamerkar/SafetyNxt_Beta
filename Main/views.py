import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import FormView
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from .forms import ContactForm, RouteFrom
from .models import Contact
from .utils import send_email_to_client
from django.contrib import messages
from .functions import get_location, get_latitude_longitude
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from .forms import RouteFrom
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from geopy import Nominatim
import logging
from django.http import JsonResponse, HttpResponseRedirect, request
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

'''
    Total 5 Routes 
        - LandingPage      : Nav, MainVideo/ MainModel, Services, Features, Contact Form, Testimonials, Footer 
        - About Page       : Nav, About Content, Footer 
        - LogInSignUp Page : AllAuth
        - GetLLs Page      : Formed based page to take start location and end location from the user along with the Start Monitoring Button 
        - Map Page         : Here the results will be displayed
        
    Total 2 Forms 
        - Contact Us : On LandingPage  
        - get_loc    : On GetLLs Page    
'''


class LandingPage(FormView):
    template_name = 'landingPage.html'
    form_class = ContactForm
    success_url = '/'  # Redirect URL after successful form submission


    def form_valid(self, form):
        form.save()  # This saves the form data to the database using the model

        # To send the contact mail
        ls_email = []
        email = form.cleaned_data['email']
        fname = form.cleaned_data['fname']
        # To get the latest mail
        ls_email.append(email)

        # Calling the actual function
        send_email_to_client(ls_email,fname)

        # To avoid sending mail to the previous users
        ls_email.clear()

        messages.info(self.request,'Your message has been successfully submitted !! ')

        return super().form_valid(form)




# AboutUs is a TemplateView since we just hv to render a simple template and dont have to perform form based or data retrival frm the models operations
# Creating the About Us Page
class AboutUs(TemplateView):

    template_name = 'about.html'

class Main(TemplateView):
    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve values from session
        start = self.request.session.get('start_lls')
        end = self.request.session.get('end_lls')

        context['start_lls'] = start
        context['end_lls'] = end

        return context

@method_decorator(csrf_exempt, name='dispatch')
class Map(TemplateView):
    template_name = 'menu.html'


@csrf_exempt
def get_coordinates(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Access the data directly
            from_lat = data.get('fromLat')
            from_lon = data.get('fromLon')
            to_lat = data.get('toLat')
            to_lon = data.get('toLon')

            print(f"From Lat: {from_lat}, From Lon: {from_lon}")
            print(f"To Lat: {to_lat}, To Lon: {to_lon}")

            return JsonResponse({'status':'success'})

        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': f'Invalid JSON format: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid Request Method'})
