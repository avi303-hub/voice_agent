from django.db import models

class VoiceQuery(models.Model):
    query = models.TextField()
    response = models.TextField()
    audio_file = models.FileField(upload_to="audio/")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query