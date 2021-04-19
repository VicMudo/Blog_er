from django.db import models
from django.conf import settings

class SearchQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query[:10]
    
    class Meta:
        verbose_name_plural = "Search Queries"
