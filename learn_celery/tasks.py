from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

@shared_task
def add(x, y):
    time.sleep(1)
    return x + y


@shared_task
def send_email_task(subject, template_name, context, recipient_list, pdf_content=None):
    """Send email with subject and template with dynamic content"""

    html_message = render_to_string(f'{template_name}.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, recipient_list)
    email.attach_alternative(html_message, 'text/html')
    
    if pdf_content:
        # TODO: Later need to implement pdf attachement if needed
        # email.attach('invoice.pdf', pdf_content, 'application/pdf')
        ...
    email.send()
    return f'Email sent to {recipient_list}'

