# myapp/views/receipt_views.py
from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from backend_api.models import Receipt
from backend_api.serializers import ReceiptSerializer
from backend_api.filters import ReceiptFilter
from rest_framework.permissions import IsAuthenticated

class ReceiptListCreateView(generics.ListCreateAPIView):
    queryset = Receipt.objects.all().order_by("payment_date").distinct()
    serializer_class = ReceiptSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReceiptFilter
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = ReceiptSerializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ReceiptSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user).order_by("payment_date").distinct()

class ReceiptUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user).order_by("payment_date").distinct()
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=204)