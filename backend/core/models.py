from django.db import models

class JoinCommunity(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name