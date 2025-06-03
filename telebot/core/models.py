from django.db import models

class VideoID(models.Model):
    file_id = models.CharField(max_length=255)

    def __str__(self):
        return self.file_id
