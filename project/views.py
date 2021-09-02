from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets
from rest_framework import generics, permissions
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

# Create your views here.

# Filter


class ContractFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    start_date = filters.DateFilter(field_name="payment_due", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="payment_due", lookup_expr="lte")
    payment_due = filters.DateFilter(field_name="payment_due", lookup_expr="date")

    class Meta:
        model = Contract
        fields = ['status', 'amount', 'min_amount', 'max_amount', 'payment_due', 'start_date', 'end_date']


class EventFilter(filters.FilterSet):
    min_attendees = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_attendees = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    start_date = filters.DateFilter(field_name="event_date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="event_date", lookup_expr="lte")
    event_date = filters.DateFilter(field_name="event_date", lookup_expr="date")

    class Meta:
        model = Event
        fields = ['attendees', 'min_attendees', 'max_attendees', 'event_date', 'start_date', 'end_date']


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated, IsSaleTeam | IsStaff)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name']

    def get_queryset(self):
        return Client.objects.all()


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = (permissions.IsAuthenticated, IsSaleTeam | IsStaff)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter

    def get_queryset(self):
        return Contract.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, EventAcces | IsSupportTeam)
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_queryset(self):
        return Event.objects.all()


class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Status.objects.all()
