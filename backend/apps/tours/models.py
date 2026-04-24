from django.db import models
from apps.destinations.models import Destination


class DifficultyLevel(models.TextChoices):
    EASY = 'easy', 'Easy'
    MODERATE = 'moderate', 'Moderate'
    CHALLENGING = 'challenging', 'Challenging'
    EXTREME = 'extreme', 'Extreme'


class TourCategory(models.TextChoices):
    ADVENTURE = 'adventure', 'Adventure'
    CULTURAL = 'cultural', 'Cultural'
    WILDLIFE = 'wildlife', 'Wildlife'
    BEACH = 'beach', 'Beach'
    CITY = 'city', 'City Tour'
    FOOD = 'food', 'Food & Culinary'
    PHOTOGRAPHY = 'photography', 'Photography'
    WELLNESS = 'wellness', 'Wellness & Spa'


class Tour(models.Model):
    title = models.CharField(max_length=300)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tours')
    category = models.CharField(max_length=20, choices=TourCategory.choices)
    difficulty = models.CharField(max_length=20, choices=DifficultyLevel.choices, default=DifficultyLevel.EASY)
    description = models.TextField()
    itinerary = models.TextField(blank=True)
    duration_days = models.PositiveIntegerField()
    max_group_size = models.PositiveIntegerField(default=15)
    min_age = models.PositiveIntegerField(default=0)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='tours/', null=True, blank=True)
    image_url = models.URLField(blank=True)
    includes = models.TextField(blank=True, help_text='Comma-separated inclusions')
    excludes = models.TextField(blank=True, help_text='Comma-separated exclusions')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tours'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        if self.discount_percent:
            return self.price_per_person * (1 - self.discount_percent / 100)
        return self.price_per_person

    @property
    def includes_list(self):
        return [i.strip() for i in self.includes.split(',') if i.strip()]

    @property
    def excludes_list(self):
        return [e.strip() for e in self.excludes.split(',') if e.strip()]


class TourDate(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='available_dates')
    start_date = models.DateField()
    end_date = models.DateField()
    available_spots = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tour_dates'
        ordering = ['start_date']

    def __str__(self):
        return f"{self.tour.title} — {self.start_date}"

    @property
    def is_sold_out(self):
        return self.available_spots == 0
