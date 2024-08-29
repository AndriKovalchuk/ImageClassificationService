from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    file = models.FileField(upload_to='documents/')  # збереження файлу
    original_name = models.CharField(max_length=255, blank=False, null=True)
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.original_name or self.file.name


class QueryHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
