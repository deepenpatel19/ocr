from django.db import models

# Create your models here.


class UploadImage(models.Model):
    name = models.ImageField()

    def __str__(self):
        return str(self.id)
