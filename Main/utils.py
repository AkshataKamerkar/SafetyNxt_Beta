from django.core.mail import send_mail
from django.conf import settings
def send_email_to_client(email,fname):

    subject = "Thank You for Contacting Us!"
    message ='''
Hello {},

Thanks for getting in touch! We've received your message and are eager to assist you. Our team is currently reviewing your inquiry and will reach out to you shortly.

Your patience is truly appreciated. If there's any additional information you'd like to share or if you have any urgent matters, feel free to reach out directly to us at ai.safetynxt@gmail.com .
    
Thanks again for reaching out to SafetyNxt. We're committed to providing you with the best possible support.

Best Regards,    
    '''.format(fname)
    from_email = settings.EMAIL_HOST_USER


    send_mail(subject,message,from_email,email)