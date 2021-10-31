from django.db import models

# Create your models here.
class list_index(models.Model):
    author = models.ForeignKey("auth.user",on_delete=models.CASCADE)
    date = models.DateField(name="added_date",auto_now=True)

class customer_food(models.Model):
    customer = models.CharField(max_length=70,null=True)

class customer_liesure(models.Model):
    customer = models.CharField(max_length=70,null=True)

class customer_shopping(models.Model):
    customer = models.CharField(max_length=70,null=True)

class liesure(models.Model):
    liesure_date = models.DateField()
    liesure_spent = models.FloatField(null=False)

class nourriture(models.Model):
    nourriture_date = models.DateField()
    nourriture_spent = models.FloatField(null=False)

class shopping(models.Model):
    shopping_date = models.DateField()
    shopping_spent = models.FloatField(null=False)


# interacting with models
"""
Ex. adding new customer into customer_liesure table
from index.models import customer_liesure
new_cust=customer_liesure()
new_cust.customer='grubers'

In [33]: new_cust.customer
Out[33]: 'grubers'

To save:
new_cust.save()

OR you can to save with:
In [35]: other_cust=customer_liesure(customer="parc")

In [36]: other_cust.save()

In [37]: 

For loop example:
In [74]: data=customer_liesure.objects.all()

In [75]: for i in data:
    ...:     print(i.customer)
    ...: 
grubers
parc


"""