from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    @property
    def events_booked_ids(self):
        list_ids = []
        for room in self.rooms.all():
            list_ids+=room.events.all().values_list('pk', flat=True)
        return set(list_ids)
            

    def is_booked_events(self, event_id):
        for room in self.rooms.all():
            event_found = room.events.filter(pk=event_id)
            if event_found.count() != 0:
                return True, room
        return False, None