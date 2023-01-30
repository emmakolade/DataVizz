from django.db import models
from django.core.validators import FileExtensionValidator
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class DataFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='uploads/', validators=[FileExtensionValidator(['csv', 'xls', 'xlsx'])])
    timestamp = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # Check if the file is older than one hour
    #     one_hour_ago = timezone.now() - timedelta(hours=1)
    #     time_stamp=timezone.make_aware(self.timestamp)
    #     if self.pk and self.timestamp < one_hour_ago:
    #         self.file.delete()
