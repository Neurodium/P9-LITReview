from django.db import models
from authentication.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    IMAGE_MAX_SIZE = (400, 400)

    def __str__(self):
        return str(self.title)


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='ticket')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')

    def __str__(self):
        return str(self.headline)

    def class_name(self):
        return self.__class__.__name__


class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank=True)
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_user', blank=True)

    def __str__(self):
        return str(self.user.username) + "_" + str(self.followed_user.username)

    class Meta:
        unique_together = ('user', 'followed_user',)




