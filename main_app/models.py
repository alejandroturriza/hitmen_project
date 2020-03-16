from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

HIT_STATUS_CHOICES = (
    (1, 'Assigned'),
    (2, 'Failed'),
    (3, 'Complete')
)


class Hit(models.Model):
    assignee = models.ForeignKey(User, related_name='hit_assignee', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    title = models.CharField(max_length=150, null=False)
    status = models.IntegerField(choices=HIT_STATUS_CHOICES, null=True, blank=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('hit_detail_url', kwargs={'id': self.id})
