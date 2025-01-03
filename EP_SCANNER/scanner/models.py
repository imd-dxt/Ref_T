from django.db import models
from django.utils import timezone

class Scan(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    
    target_url = models.URLField(max_length=500)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    report = models.JSONField(default=dict)
    technologies = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"Scan of {self.target_url} ({self.status})"

class Alert(models.Model):
    RISK_LEVELS = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Informational', 'Informational'),
    ]

    scan = models.ForeignKey(Scan, related_name='alerts', on_delete=models.CASCADE)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='Informational')
    confidence = models.CharField(max_length=20, default='Unknown')
    name = models.CharField(max_length=200, default='Unnamed Alert')
    description = models.TextField(default='No description provided.')
    url = models.URLField(max_length=500, default='http://example.com')
    param = models.CharField(max_length=200, blank=True, default='')
    evidence = models.TextField(blank=True, default='')
    solution = models.TextField(blank=True, default='')
    reference = models.TextField(blank=True, default='')
    cwe_id = models.CharField(max_length=50, blank=True, default='N/A')
    wasc_id = models.CharField(max_length=50, blank=True, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.risk_level} - {self.name}"
