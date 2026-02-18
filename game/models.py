from django.db import models

class Round(models.Model):
    average = models.FloatField(default=0)
    loser = models.CharField(max_length=50, blank=True)

class Entry(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(default=0)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)