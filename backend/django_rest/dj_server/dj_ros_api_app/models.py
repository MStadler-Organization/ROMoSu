from django.db import models


# Create your models here.

class TopicList(models.Model):
    """Stores the list of topics as JSON objects"""
    topiclist = models.TextField()

    def __str__(self):
        return self.topiclist
