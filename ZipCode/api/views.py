from rest_framework import generics
from .serializers import UserEntrySerializer, ZipCodeCounterSerializer
from .models import UserEntry, ZipCodeCounter


class UserEntryPost(generics.CreateAPIView):
    queryset = UserEntry.objects.all()
    serializer_class = UserEntrySerializer        


class UserEntries(generics.ListAPIView):
    queryset = UserEntry.objects.all()
    serializer_class = UserEntrySerializer

class UserEntry(generics.RetrieveAPIView):
    queryset = UserEntry.objects.all()
    serializer_class = UserEntrySerializer 

class ZipCodeCounters(generics.ListAPIView):
    queryset = ZipCodeCounter.objects.all()
    serializer_class = ZipCodeCounterSerializer

class ZipCodeCounter(generics.RetrieveAPIView):
    queryset = ZipCodeCounter.objects.all()
    serializer_class = ZipCodeCounterSerializer


