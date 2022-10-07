from django.db import models

class Room(models.Model):
    capacity = models.PositiveIntegerField()
    events = models.ManyToManyField('Event', related_name = 'rooms', blank = True)
    persons = models.ManyToManyField('booking.Customer', related_name = 'rooms', blank = True)

    def __str__(self):
        return f'{self.id} - {self.capacity}'

    @property
    def count_events(self):
        return self.events.all().count()
    
    @property
    def count_persons(self):
        return self.persons.all().count()

    @property
    def avilable_space(self):
        return self.capacity - self.count_persons

    @property
    def is_available(self):
        if self.avilable_space == 0:
            return False
        return True