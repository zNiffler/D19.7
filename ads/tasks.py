from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ads.models import Response

@shared_task
def send_message_res(pk):
    response = Response.objects.get(pk=pk)
    html_content = render_to_string(
        'response_created.html',
        {
            'response': response,
            'link': f'{settings.SITE_URL}/accounts/responses/',
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{response.author} {response.date_create.strftime("%Y-%M-%d")}',
        body=response.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[response.ad.author.email],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()