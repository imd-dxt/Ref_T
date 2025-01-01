from django.db import models

class ScanResult(models.Model):
    url = models.URLField()
    scan_date = models.DateTimeField()
    high_risk_count = models.IntegerField(default=0)
    medium_risk_count = models.IntegerField(default=0)
    low_risk_count = models.IntegerField(default=0)
    informational_risk_count = models.IntegerField(default=0)
    total_alerts = models.IntegerField(default=0)
    report = models.JSONField()

    def __str__(self):
        return self.url
