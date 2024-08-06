from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=10)
    quantity = models.IntegerField()
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name
