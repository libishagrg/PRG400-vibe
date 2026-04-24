from django.db import models


class Continent(models.TextChoices):
    AFRICA = 'AF', 'Africa'
    ANTARCTICA = 'AN', 'Antarctica'
    ASIA = 'AS', 'Asia'
    EUROPE = 'EU', 'Europe'
    NORTH_AMERICA = 'NA', 'North America'
    OCEANIA = 'OC', 'Oceania'
    SOUTH_AMERICA = 'SA', 'South America'


class Destination(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=2, choices=Continent.choices)
    description = models.TextField()
    highlights = models.TextField(blank=True, help_text='Comma-separated highlights')
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    image_url = models.URLField(blank=True)
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'destinations'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country}"

    @property
    def highlight_list(self):
        return [h.strip() for h in self.highlights.split(',') if h.strip()]
