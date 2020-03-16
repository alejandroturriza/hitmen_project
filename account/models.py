from django.db import models
from django.contrib.auth.models import User


HITMAN_STATUS_CHOICES = (
    (1, 'Active'),
    (2, 'Inactive')
)


class Hitman(models.Model):
    user = models.OneToOneField(User, related_name='hitman_user', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username
