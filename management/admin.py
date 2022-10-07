from django.contrib import admin

# Register your models here.
from .models import Event, Room


# Register your models here.
@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomModelAdmin(admin.ModelAdmin):
    pass