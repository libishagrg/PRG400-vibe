from django.db import models
from django.conf import settings
from apps.tours.models import Tour, TourDate


class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'
    COMPLETED = 'completed', 'Completed'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    tour_date = models.ForeignKey(TourDate, on_delete=models.SET_NULL, null=True, related_name='bookings')
    number_of_travelers = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    special_requests = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.pk} — {self.user.email} / {self.tour.title}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.total_price = self.tour.discounted_price * self.number_of_travelers
            if self.tour_date and self.tour_date.available_spots >= self.number_of_travelers:
                self.tour_date.available_spots -= self.number_of_travelers
                self.tour_date.save()
        super().save(*args, **kwargs)
