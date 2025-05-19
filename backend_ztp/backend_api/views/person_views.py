from rest_framework import viewsets
from backend_api.models import Person
from backend_api.serializers import PersonSerializer
from rest_framework.permissions import IsAuthenticated

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Person.objects.filter(user=self.request.user)
