from django.db import models
from django.db.models import F, Sum ,Count
class Event(models.Model):
    name = models.CharField(max_length=256)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @property
    def capacity(self):
        return self.rooms.all().annotate(avialable = F('capacity') - Count('persons')).aggregate(total = Sum('avialable')).get('total',0)

    @property
    def is_available(self):
        if self.capacity == 0:
            return False
        return True

    @property
    def room_available(self):
        for room in self.rooms.all():
            if room.is_available:
                return room
        return None
    