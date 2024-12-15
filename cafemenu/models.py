from django.db import models

class Menu_items (models.Model):
    item=models.CharField(max_length=100)
    price=models.IntegerField()
    price2= models.IntegerField(default=0, blank=True)


