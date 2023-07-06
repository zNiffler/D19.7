from django.contrib.auth.models import User
from django.db import models


class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codes')
    code_value = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s code {self.code_value}"
