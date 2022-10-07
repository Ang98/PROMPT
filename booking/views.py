from rest_framework.decorators import action
from rest_framework import viewsets, permissions , status
from rest_framework.response import Response

from management.models import Room, Event
from management.serializers import EventSerializer

from .models import Customer
from .serializers import CustomerSerializer , CustomerBookEventSerializer


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=True,methods=['POST'],url_path='book_event/(?P<event_id>[^/.]+)')
    def book_event(self,request,pk, event_id = None):
        customer = self.get_object()
        event = Event.objects.get(pk = int(event_id))
        serializer = CustomerBookEventSerializer(event)
        serializer_customer = serializer.book_event(customer)
        return Response(serializer_customer.data)

    @action(detail=True,methods=['POST'],url_path='cancel_event/(?P<event_id>[^/.]+)')
    def cancel_event(self,request,pk, event_id = None):
        customer = self.get_object()
        is_booked, room = customer.is_booked_events(int(event_id))
        if is_booked:
            room.persons.remove(customer)
            return Response(CustomerSerializer(customer).data)
        return Response({'detail' : "CUSTOMER IS NOT BOOKED FOR THIS EVENT"})
    
    @action(detail=True,methods=['GET'])
    def events_available(self,request,pk):
        customer = self.get_object()
        events = Event.objects.filter(is_private=False).exclude(pk__in=customer.events_booked_ids)
        return Response(EventSerializer(events, many = True).data)