from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Tour, TourDate
from .serializers import TourSerializer, TourListSerializer, TourDateSerializer


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.filter(is_active=True).select_related('destination')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['destination', 'category', 'difficulty', 'is_featured']
    search_fields = ['title', 'description', 'destination__name', 'destination__country']
    ordering_fields = ['price_per_person', 'rating', 'duration_days', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        return TourSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'by_destination']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        tours = Tour.objects.filter(is_featured=True, is_active=True).select_related('destination')
        serializer = TourListSerializer(tours, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        from .models import TourCategory
        return Response([{'value': c.value, 'label': c.label} for c in TourCategory])

    @action(detail=True, methods=['get'])
    def dates(self, request, pk=None):
        tour = self.get_object()
        dates = TourDate.objects.filter(tour=tour, is_active=True)
        serializer = TourDateSerializer(dates, many=True)
        return Response(serializer.data)


class TourDateViewSet(viewsets.ModelViewSet):
    queryset = TourDate.objects.filter(is_active=True)
    serializer_class = TourDateSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
