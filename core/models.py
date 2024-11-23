from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime, timedelta

class Tasks(models.Model):
    user =  models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
                            
class Invitation(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = datetime.now() + timedelta(days=7)  # 7-day expiration
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return datetime.now() > self.expires_at
    

    
    

