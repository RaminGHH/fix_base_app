from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User

@receiver(post_save, sender=User, dispatch_uid='accounts.create_profile')
def create_profile(sender, instance, created, raw=False, using='default', **kwargs):
    if created and not raw:
        Profile.objects.using(using).get_or_create(user=instance)