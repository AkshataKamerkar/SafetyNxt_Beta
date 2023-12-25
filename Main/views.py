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
# LandinPage is a FormView since we have to add a Contact Us form in it
class LandingPage(TemplateView):         # Jb tk form define nhi krte tb tk
                                         # FormView mt do, if diya toh django usse load hi nhi krta

    template_name = 'landingPage.html'

# AboutUs is a TemplateView since we just hv to render a simple template and dont have to perform form based or data retrival frm the models operations
# Creating the About Us Page
class AboutUs(TemplateView):

    template_name = 'about.html'

# FormView coz here we have to take new users info and register it in our db as well as retrive and confirm the info of existing user
class LogInSignUp(TemplateView):

    template_name = 'log.html'

# After successful login user will be redirected to this page, we will get users location info from this page
class GetLLs(FormView):

    template_name = 'getInfo.html'