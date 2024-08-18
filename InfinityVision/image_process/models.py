from django.contrib.auth.models import User
from django.db import models


class IMAGE(models.Model):
    file = models.FileField(upload_to='Images/')
    original_name = models.CharField(max_length=255, blank=True, null=True)
    predicted_class = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.original_name or self.file.name
