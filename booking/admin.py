from django.contrib import admin

# Register your models here.
from .models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    pass