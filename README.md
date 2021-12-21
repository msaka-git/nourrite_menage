# nourrite_menage
Calculate monthly expenses from excel file
Webapp first structure. Will be merged with master repository (webapp).

## ORM database usage

Ex. adding new customer into customer_liesure table
```
from index.models import customer_liesure
new_cust=customer_liesure()
new_cust.customer='grubers'

In [33]: new_cust.customer
Out[33]: 'grubers'

To save:
new_cust.save()
```

OR you can to save with:
```
In [35]: other_cust=customer_liesure(customer="parc")

In [36]: other_cust.save() 
```
For loop example:
```
In [74]: data=customer_liesure.objects.all()

In [75]: for i in data:
    ...:     print(i.customer)
    ...: 
grubers
parc
```
