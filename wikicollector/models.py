from django.db import models


class RecentChange(models.Model):
    title = models.TextField()
    country = models.TextField(null=True)
    city = models.TextField(null=True)
    user = models.TextField()
    bot = models.BooleanField()
    type = models.CharField(max_length=256)
    timestamp = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
