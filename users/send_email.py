
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

settings.configure()

# def send_email():
#     subject = 'Sujet de l\'e-mail'
#     message = render_to_string('email_template.html', {'context_variable': 'valeur'})
#     to_email = ['destinataire@example.com']

#     email = EmailMessage(subject, message, to=to_email)
#     email.content_subtype = 'html'
#     email.send()

#     return HttpResponse('E-mail envoyé avec succès!')

# send_email()

def send_email_account_creation(username, email):
    html_message = render_to_string("email.html", {'username':username})
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(subject="Account creation", body=plain_message,
    from_email="efomenakuete@gmail.com", to=[email]
                                     )
    message.attach_alternative(html_message, "text/html")
    message.send()

send_email_account_creation("emel", "emeldamigrice@gmail.com")
