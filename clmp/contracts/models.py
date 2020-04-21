from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contract(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    participant = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    contractStatus = models.TextField()

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50]