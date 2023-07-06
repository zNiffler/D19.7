from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from ads.res import CAT


class Ad(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CAT)
    date_create = models.DateTimeField(auto_now_add=True)
    content = models.FileField(upload_to='content/', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad', args=[str(self.id)])


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='response')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    accept = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:20] + '...'

    def accepted(self):
        self.accept = True
        self.save()
