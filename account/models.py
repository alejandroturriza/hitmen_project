from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Hitman(models.Model):
    user = models.OneToOneField(User, related_name='hitman_user', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('hitmen_detail_url', kwargs={'id': self.id})
