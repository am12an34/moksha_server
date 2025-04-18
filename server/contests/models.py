from django.db.models import Model, AutoField, CharField, BooleanField, ForeignKey, DateTimeField, CASCADE
from teams.models import Team
from django.contrib.auth.models import User


class Contest(Model):
    id = AutoField(primary_key=True)
    club_slug = CharField(max_length=30, null=False)
    contest_slug = CharField(max_length=30, null=False)
    is_solo = BooleanField(null=False)

    def __str__(self):
        return str(self.id)


class SoloContestRegistration(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(
        User,
        related_name='registered_solo_contests',
        on_delete=CASCADE,
        null=False,
        db_column='user'
    )
    contest = ForeignKey(
        Contest, related_name='registered_users',
        on_delete=CASCADE,
        null=False,
        db_column='contest'
    )
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class TeamContestRegistration(Model):
    id = AutoField(primary_key=True)
    team = ForeignKey(
        Team,
        related_name='registered_team_contests',
        on_delete=CASCADE, null=False, db_column='team'
    )
    contest = ForeignKey(
        Contest,
        related_name='registered_teams',
        on_delete=CASCADE, null=False, db_column='contest'
    )
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class TeamContestUserRegistration(Model):
    id = AutoField(primary_key=True)
    team_contest_registration = ForeignKey(
        TeamContestRegistration,
        related_name='registered_members',
        on_delete=CASCADE, null=False, db_column='team_contest_registration'
    )
    user = ForeignKey(
        User,
        related_name='team_contest_registrations',
        on_delete=CASCADE, null=False, db_column='user'
    )

    def __str__(self):
        return str(self.id)
