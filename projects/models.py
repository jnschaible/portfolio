from django.db import models
from django.utils.timezone import now


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=50)
    images = models.ManyToManyField('Image', related_name='projects')
    thumbnail = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Image(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    caption = models.CharField(max_length=140)

    def __str__(self):
        return self.title
