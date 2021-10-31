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