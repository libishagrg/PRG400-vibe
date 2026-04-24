from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.tours.models import Tour


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    travel_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        unique_together = ['user', 'tour']

    def __str__(self):
        return f"{self.user.email} — {self.tour.title} ({self.rating}★)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_tour_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self._update_tour_rating()

    def _update_tour_rating(self):
        from django.db.models import Avg, Count
        stats = Review.objects.filter(tour=self.tour).aggregate(
            avg=Avg('rating'), count=Count('id')
        )
        self.tour.rating = round(stats['avg'] or 0, 2)
        self.tour.total_reviews = stats['count']
        self.tour.save(update_fields=['rating', 'total_reviews'])
