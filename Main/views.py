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


'''
    Total 5 Routes 
        - LandingPage      : Nav, MainVideo/ MainModel, Services, Features, Contact Form, Testimonials, Footer 
        - About Page       : Nav, About Content, Footer 
        - LogInSignUp Page : Nav, LogIn/SignUp Form, Footer 
        - GetLLs Page      : Formed based page to take start location and end location from the user along with the Start Monitoring Button 
        - Map Page         : Here the results will be displayed
        
    Total 3 Forms 
        - Contact Us : On LandingPage 
        - Login Form : On LogInSignUp Page 
        - get_loc    : On GetLLs Page    
'''

start_lls = None
end_lls = None

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_lls = self.request.session.get('start_lls')
        end_lls = self.request.session.get('end_lls')


        context['start_lls'] = start_lls
        context['end_lls'] = end_lls

        return context




# AboutUs is a TemplateView since we just hv to render a simple template and dont have to perform form based or data retrival frm the models operations
# Creating the About Us Page
class AboutUs(TemplateView):

    template_name = 'about.html'

# FormView coz here we have to take new users info and register it in our db as well as retrive and confirm the info of existing user
class LogInSignUp(TemplateView):

    template_name = 'log.html'



class GetLLs(FormView):

    template_name = 'map.html'
    form_class = RouteFrom
    success_url = 'menu'

    def form_valid(self, form):

        start = form.cleaned_data['start']
        destination = form.cleaned_data['destination']

        start_lls = get_latitude_longitude(start)
        end_lls = get_latitude_longitude(destination)

        self.start_lls = start_lls
        self.end_lls = end_lls

        return redirect('main:menu')


# Main Page
class Main(TemplateView):

    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_lls = self.request.session.get('start_lls')
        end_lls = self.request.session.get('end_lls')

        context['start_lls'] = [40.7128,-74.0060]
        context['end_lls'] = [ 34.0522,-118.2437]

        return context

