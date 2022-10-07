import json
from rest_framework import status
from rest_framework.test import APITestCase

from booking.models import Customer
from management.models import Event, Room


class BusinesTestCase(APITestCase):
    def setUp(self):
        event = Event(
            name = "event 1",
            is_private = False
        )
        event.save()

        room_with_event = Room(capacity = 10)
        room_with_event.save()
        room_with_event.events.add(event)
        room_with_event.save()

        room_without_event = Room(capacity = 15)
        room_without_event.save()

        self.event = event
        self.room_with_event = room_with_event
        self.room_without_event = room_without_event

    #Requirement 1
    def test_create_room_x_capacity(self):
        AMOUNT = 10
        response = self.client.post(f'/management/room/capacity/{AMOUNT}/')
        last_room = Room.objects.all().last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AMOUNT, last_room.capacity)

    #Requirement 2
    def test_create_event_public(self):
        data = {"name": "event public"}
        response = self.client.post(f'/management/event/',data)
        last_event = Event.objects.all().last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['name'], last_event.name)
        self.assertEqual(False, last_event.is_private)

    def test_create_event_private(self):
        data = {"name": "event private", "is_private": True}
        response = self.client.post(f'/management/event/',data)
        last_event = Event.objects.all().last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['name'], last_event.name)
        self.assertEqual(data['is_private'], last_event.is_private)

    #Requirement 3
    def test_delete_room_without_events(self):
        id = self.room_without_event.id
        response = self.client.delete(f'/management/room/{id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_room_with_events(self):
        id = self.room_with_event.id
        response = self.client.delete(f'/management/room/{id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        self.assertEqual(json.loads(response.content), {"detail": "THIS ROOM HAS EVENTS YET"})

class CustomerTestCase(APITestCase):
    def setUp(self):
        event = Event(
            name = "event 1",
            is_private = False
        )
        event.save()

        event_private = Event(
            name = "event private",
            is_private = True
        )
        event_private.save()

        event_full = Event(
            name = "event full",
            is_private = False
        )
        event_full.save()

        customer_with_event = Customer(name = "customer with event")
        customer_with_event.save()

        room_full = Room(capacity = 1)
        room_full.save()
        room_full.events.add(event_full)
        room_full.persons.add(customer_with_event)
        room_full.save()

        customer = Customer(name = "customer 1")
        customer.save()

        self.event = event
        self.customer = customer
        self.event_private = event_private
        self.event_full = event_full
        self.customer_with_event = customer_with_event

    #Requirement 4
    def test_customer_book_event(self):
        id_customer = self.customer.id
        id_event = self.event.id
        response = self.client.post(f'/booking/customer/{id_customer}/book_event/{id_event}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_customer_book_event_private(self):
        id_customer = self.customer.id
        id_event = self.event_private.id
        response = self.client.post(f'/booking/customer/{id_customer}/book_event/{id_event}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response.render()
        self.assertEqual(json.loads(response.content), {'message':"THIS EVENT  IS PRIVATE"})

    def test_customer_book_event_full(self):
        id_customer = self.customer.id
        id_event = self.event_full.id
        response = self.client.post(f'/booking/customer/{id_customer}/book_event/{id_event}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response.render()
        self.assertEqual(json.loads(response.content), {'message':"THIS EVENT  IS FULL"})

    #Requirement 5
    def test_customer_cancel_book_event(self):
        id_customer = self.customer_with_event.id
        id_event = self.event_full.id
        response = self.client.post(f'/booking/customer/{id_customer}/cancel_event/{id_event}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Requirement 6
    def test_customer_see_available_event(self):
        id_customer = self.customer.id
        response = self.client.get(f'/booking/customer/{id_customer}/events_available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

