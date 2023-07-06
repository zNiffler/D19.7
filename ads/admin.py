from django.contrib import admin

from ads.models import Ad, Response

admin.site.register(Ad)
# admin.site.register(AdContent)
admin.site.register(Response)
