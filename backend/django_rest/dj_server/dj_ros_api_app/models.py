from django.db import models


# Create your models here.

class TopicList(models.Model):
    """Stores the list of topics as JSON objects"""
    topiclist = models.TextField()

    def __str__(self):
        return self.topiclist


class SuMType(models.Model):
    """Stores the different Types of SuM"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MonitoringConfig(models.Model):
    """Stores the monitoring configurations"""
    name = models.CharField(max_length=200)
    save_type = models.CharField(max_length=200)
    sum_type_id = models.IntegerField
    property_tree = models.TextField()
    frequencies = models.TextField()
    ecore_file = models.TextField()

    def __str__(self):
        return self.name
