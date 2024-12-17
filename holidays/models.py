from django.db import models

class Holiday(models.Model):
    country = models.CharField(max_length=2)
    year = models.IntegerField()
    month = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    type = models.CharField(max_length=255)

    class Meta:
        unique_together = ('country', 'year', 'month', 'name')

