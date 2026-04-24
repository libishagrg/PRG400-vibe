from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking, BookingStatus
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all().select_related('user', 'tour', 'tour_date')
        return Booking.objects.filter(user=user).select_related('tour', 'tour_date')

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'cancel']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.user != request.user and not request.user.is_staff:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        if booking.status == BookingStatus.CANCELLED:
            return Response({'detail': 'Booking is already cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
        if booking.status == BookingStatus.COMPLETED:
            return Response({'detail': 'Cannot cancel a completed booking.'}, status=status.HTTP_400_BAD_REQUEST)
        if booking.tour_date:
            booking.tour_date.available_spots += booking.number_of_travelers
            booking.tour_date.save()
        booking.status = BookingStatus.CANCELLED
        booking.save()
        return Response(BookingSerializer(booking).data)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        bookings = Booking.objects.filter(user=request.user).select_related('tour', 'tour_date')
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
