
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from management.models import Room, Event
from management.serializers import RoomCustomerSerializer
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    rooms = RoomCustomerSerializer(read_only=True, many=True)
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerBookEventSerializer(serializers.ModelSerializer):
    capacity = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    room_available = serializers.ReadOnlyField()
    class Meta:
        model = Event
        fields = '__all__'
    
    def validate(self, validate_data):
        is_private = validate_data.get('is_private',None)
        is_available = validate_data.get('is_available',None)
        if is_private :
            raise ValidationError({'message':"THIS EVENT  IS PRIVATE"})
        if not is_available :
            raise ValidationError({'message':"THIS EVENT  IS FULL"})

        return validate_data

    def book_event(self, customer):
        self.validate(self.data)
        room  = self.data['room_available']
        customer.rooms.add(room)
        customer.save()
        return CustomerSerializer(customer)

    
        
