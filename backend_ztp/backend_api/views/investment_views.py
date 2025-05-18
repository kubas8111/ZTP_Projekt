from rest_framework import viewsets
from backend_api.models import Instrument, Invest, WalletSnapshot
from backend_api.serializers import (
    InstrumentSerializer,
    InvestSerializer,
    WalletSnapshotSerializer,
)


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return Instrument.objects.filter(user=self.request.user)
        


class InvestViewSet(viewsets.ModelViewSet):
    queryset = Invest.objects.all()
    serializer_class = InvestSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return Invest.objects.filter(user=self.request.user)


class WalletSnapshotViewSet(viewsets.ModelViewSet):
    queryset = WalletSnapshot.objects.all()
    serializer_class = WalletSnapshotSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return WalletSnapshot.objects.filter(user=self.request.user)
    
    