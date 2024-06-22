from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
from django_react.stripe import Stripe, StripeSource
from django.dispatch import receiver
from django.utils import timezone
from backend_django.models import Company

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    customer_id = models.CharField(max_length=500, null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", default=os.path.join(settings.BASE_DIR, "media/profile_photos/generic.png"))
    paid = models.BooleanField(default=False) # Will be used to check if a user subscribed or not
    pageview = models.IntegerField(default=0)
    

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"





class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default = timezone.now)

class Visited(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default = timezone.now)


# @receiver(models.signals.post_save, sender=User)
# def create_stripe_after_user_created(sender, instance, created, **kwargs):
#     if created:
#         stripe_id = Stripe.create_customer(instance.first_name, instance.email.lower())
#         if stripe_id[0]:
#             try:
#                 user = Profile.objects.get(user=instance)
#             except Profile.DoesNotExist:
#                 user = None
#             if user:
#                 try:
#                     user.customer_id=stripe_id[1]
#                     user.save(update_fields=["customer_id"])
#                 except Exception as e:
#                     return e