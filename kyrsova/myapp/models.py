from django.db import models


class Car(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    mark_name = models.CharField(max_length=100, default=' ')
    model_name = models.CharField(max_length=100)
    generation_name = models.CharField(max_length=100)
    equipment_name = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'data'
