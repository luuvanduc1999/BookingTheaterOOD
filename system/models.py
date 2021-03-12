from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.TextField()
    content = models.TextField()
    def __str__(self):
        return self.title
