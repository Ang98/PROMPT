from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomCustomerSerializer(serializers.ModelSerializer):
    events = serializers.SlugRelatedField(read_only=True, slug_field="name", many=True)
    class Meta:
        model = Room
        fields = ('id','events')

class RoomCreateSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(min_value=1)
    class Meta:
        model = Room
        fields = ['id', 'capacity']