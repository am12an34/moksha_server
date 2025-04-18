from django.contrib.auth.models import User
from django.db.models import Model, CharField, DateTimeField, EmailField, SmallIntegerField, ForeignKey, CASCADE


class UnverifiedAccount(Model):
    hash = CharField(primary_key=True, null=False, max_length=20)
    otp = SmallIntegerField(null=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    avatar_idx = SmallIntegerField()
    first_name = CharField(max_length=100, null=False)
    last_name = CharField(max_length=100, null=False)
    institution = CharField(max_length=100, null=False)
    phone_no = CharField(max_length=100,null=False)
    email = EmailField(unique=True, null=False)
    username = CharField(max_length=100, null=False)
    password = CharField(max_length=100, null=False)

    def __str__(self):
        return self.hash


class ForgotPasswordLink(Model):
    hash = CharField(primary_key=True, null=False, max_length=20)
    user = ForeignKey(User, related_name='forgot_otp_entries',
                      on_delete=CASCADE, null=False, db_column='user')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.hash
