from django.conf import settings
from django.db import models

# Create your models here.


class Follow(models.Model):
    CHOICE_FIELD = [('a', 'accept'), ('p', 'pending')]
    follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE, related_name="followed")
    status = models.CharField(choices=CHOICE_FIELD, max_length=1, default='p')
    follow_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed',)

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
