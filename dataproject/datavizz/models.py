from django.db import models
from django.core.validators import FileExtensionValidator
import datetime
from django.contrib.auth.models import User
# Create your models here.


class DataFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='uploads/', validators=[FileExtensionValidator(['csv', 'xls', 'xlsx'])])
    timestamp = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # Check if the file is older than one hour
    #     if datetime.datetime.utcnow() - self.timestamp > datetime.timedelta(hours=1):
    #         self.file.delete()
