from django.db import models

# Create your models here.


class Letter(models.Model):
    text = models.TextField()
    sender = models.CharField(max_length=128)
    receiver = models.CharField(max_length=128)
    postdate = models.SmallIntegerField()
    status = models.CharField(max_length=10, choices=[('D', 'draft'), ('P', 'published')], default='D')

    def __str__(self):
        return f'{self.text} {self.postdate}'
