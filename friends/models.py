from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import *


# Create your models here.
class FriendRequest(models.Model):
    """
    Model that stores friendrequest information
    """
    class Status_Choices(models.TextChoices):
        PENDING  = "pending", _("pending")
        ACCEPTED = "accepted", _("accepted")
        REJECTED = "rejected", _("rejected")
      
    request_from = models.ForeignKey(CustomUser, related_name='request_from',
                                    on_delete=models.CASCADE, help_text='friend request from user') 
    request_to = models.ForeignKey(CustomUser, related_name='request_to',
                                   on_delete=models.CASCADE, help_text='friend request to user')
    status = models.CharField(choices=Status_Choices.choices,
                              default=Status_Choices.PENDING, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.request_from.first_name} to {self.request_to.first_name} status-{self.status}"
    
    class Meta:
        verbose_name = 'FriendRequest'