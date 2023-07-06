from random import randint

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ads.models import Response
from personal.models import Code


@shared_task
def send_message_accept(pk):
    res = Response.objects.get(pk=pk)
    html_content = render_to_string(
        'response_accepted.html',
        {
            'response': res,
            'link': f'{settings.SITE_URL}/ads/{res.ad.pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Здравствуй {res.author}',
        body=res.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[res.author.email],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()


@shared_task
def send_message_singup(pk):
    code = randint(1000, 9999)
    user = User.objects.get(pk=pk)
    Code.objects.create(user=user, code_value=code)
    html_content = render_to_string(
        'email_activate.html',
        {
            'user': user,
            'link': f'{settings.SITE_URL}/accounts/{user.pk}',
            'code': code,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Здравствуй {user}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()