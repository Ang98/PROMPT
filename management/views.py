from rest_framework import viewsets, permissions , status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Room, Event
from .serializers import EventSerializer, RoomSerializer ,RoomCreateSerializer


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.AllowAny,)

class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.AllowAny,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.count_events != 0:
            return Response({'detail' : "THIS ROOM HAS EVENTS YET"})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False,methods=['POST'],url_path='capacity/(?P<number>[^/.]+)')
    def capacity(self,request,number):
        data = {"capacity":int(number)}
        serializer = RoomCreateSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)