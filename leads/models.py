from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.


class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(
        "Category",
        related_name="leads",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.first_name


def user_created_signal(instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(user_created_signal, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
