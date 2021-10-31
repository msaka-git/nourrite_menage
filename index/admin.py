from django.contrib import admin
from .models import list_index,customer_shopping,liesure,shopping,nourriture,customer_liesure,customer_food

# Register your models here.
# admin.site.register(list_index)
# admin.site.register(customer_shopping)
# admin.site.register(customer_liesure)
# admin.site.register(customer_food)
# admin.site.register(liesure)
# admin.site.register(shopping)
# admin.site.register(nourriture)
@admin.register(list_index,customer_shopping,liesure,shopping,nourriture,customer_liesure,customer_food)
class IndexAdmin(admin.ModelAdmin):
    search_fields = ['customer']
    class Meta:
        model = list_index,customer_shopping,liesure,shopping,nourriture,customer_liesure,customer_food
