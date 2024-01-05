from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import FormView
from .forms import ContactForm
from .models import Contact
from .utils import send_email_to_client

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

# Creating the Landing Page
# LandinPage is a FormView since we have to add a Contact Us form in it
# class LandingPage(FormView):         # Jb tk form define nhi krte tb tk
#                                          # FormView mt do, if diya toh django usse load hi nhi krta
#
#     template_name = 'landingPage.html'
#     form_class = contactForm
#     success_url = '/'
#
#     def form_valid(self, form):
#         new_object = contact.objects.create(
#             fname = form.cleaned_data['fname'],
#             lname = form.cleaned_data['lname'],
#             email = form.cleaned_data['email'],
#             mob = form.cleaned_data['mob'],
#             msg = form.cleaned_data['msg']
#
#         )
#
#         return super().form_valid(form)


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

        return super().form_valid(form)





# AboutUs is a TemplateView since we just hv to render a simple template and dont have to perform form based or data retrival frm the models operations
# Creating the About Us Page
class AboutUs(TemplateView):

    template_name = 'about.html'

# FormView coz here we have to take new users info and register it in our db as well as retrive and confirm the info of existing user
class LogInSignUp(TemplateView):

    template_name = 'log.html'

# After successful login user will be redirected to this page, we will get users location info from this page
class GetLLs(TemplateView):

    template_name = 'map.html'

# Main Page
class Main(TemplateView):

    template_name = 'menu.html'

