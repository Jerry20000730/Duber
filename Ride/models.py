import uuid
from django.db import models

from Account.models import DuberUser
from Duber import settings


# Create your models here.
# model for rides
class Ride(models.Model):
    class RideStatus(models.IntegerChoices):
        OPEN = 1
        CONFIRM = 2
        COMPLETE = 3

    ride_id = models.UUIDField(max_length=10, default=uuid.uuid4, editable=False, primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username', blank=False, null=False, related_name='owner')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username', blank=True, null=True, related_name='driver')


    src_addr = models.CharField(max_length=100)
    dst_addr = models.CharField(max_length=100)
    status = models.IntegerField(choices=RideStatus, default=RideStatus.OPEN)
    num_passengers_owner_party = models.PositiveIntegerField()
    num_passengers_sharer_party = models.PositiveIntegerField(default=0)
    time_created = models.TimeField(auto_now_add=True)
    time_uptate = models.TimeField(auto_now=True)
    time_complete = models.TimeField(blank=True, null=True)

    is_shareable = models.BooleanField(default=False)

    special_requests = models.TextField()


    class Meta:
        verbose_name = 'ride'
        verbose_name_plural = 'rides'

    def __str__(self):
        return "{}-owner:{}-driver:{}-src:{}-dst:{}".format(self.ride_id, self.owner, self.driver, self.src_addr, self.dst_addr)
