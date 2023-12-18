from django.shortcuts import render
from django.views.generic import TemplateView, FormView

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
# LandingPage is a TemplateView since we just hv to render a simple template and dont have to perform form based or data retrival frm the models operations
class LandingPage(FormView):


    template_name = 'landingPage.html'

# Creating the About Us Page
class AboutUs(TemplateView):

    template_name = 'about.html'

class LogInSignUp(FormView):

    template_name = 'log.html'


class GetLLs(FormView):

    template_name = 'getInfo.html'