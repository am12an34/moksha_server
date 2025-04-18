from django.contrib.auth.models import User
from django.db.models import Model, CharField, SmallIntegerField, OneToOneField, CASCADE
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.utils import timezone

# TODO: add client-side validation for usernames that are taken


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)

    tag = CharField(max_length=50, null=False)
    avatar_idx = SmallIntegerField()
    institution = CharField(max_length=100, null=False)

    # TODO: add verification for phone
    phone_no = CharField(max_length=100,unique=True, null=False)
    # password_updated_at = DateTimeField(null=False)

    role = CharField(max_length=100, default='user', null=False)

    def __str__(self):
        return self.tag


# https://docs.djangoproject.com/en/5.0/topics/signals/

# @receiver(pre_save, sender=Profile)
# def update_password_updated_at(sender, instance, **kwargs):
#     if instance.pk is None:
#         # This is a new user, set this field to creation time
#         instance.password_updated_at = timezone.now()
#     else:
#         # Check if the password field has been updated
#         original_user = User.objects.get(profile_=instance.pk)
#         if instance.password != original_user.password:
#             instance.password_updated_at = timezone.now()


# pre_save.connect(update_password_updated_at, sender=User)
