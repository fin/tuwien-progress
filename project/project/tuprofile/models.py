from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile
import uuid

class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=('user'),
                                related_name='my_profile')
    auth_key = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.auth_key:
            self.auth_key = str(uuid.uuid4())
        super(Profile, self).save()

