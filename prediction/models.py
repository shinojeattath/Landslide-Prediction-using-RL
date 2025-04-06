from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UnusualActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    activity_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} reported at {self.location}"
    
class SensorReading(models.Model):
    """Model to store sensor readings"""
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    altitude = models.FloatField()
    accel_x = models.FloatField()
    accel_y = models.FloatField()
    accel_z = models.FloatField()
    soil_moisture = models.IntegerField()
    slope = models.FloatField()
    aspect = models.FloatField()
    risk_level = models.IntegerField()  # 0: stable, 1: risk
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reading at {self.timestamp}"