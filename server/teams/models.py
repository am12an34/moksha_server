from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.db.models import Model, AutoField, IntegerField, CharField, TextField, ForeignKey, CASCADE, UniqueConstraint


class Team(Model):
    team_id = CharField(primary_key=True, max_length=100, null=False)
    team_name = TextField(null=False)
    leader = ForeignKey(User, related_name='created_team',
                        on_delete=CASCADE, null=False, db_column='leader')
    member_count = IntegerField(default=1, null=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('team_name'),
                name='unique_team_name',
            ),
        ]

    def __str__(self):
        return self.team_id


class TeamMember(Model):
    id = AutoField(primary_key=True)
    team = ForeignKey(
        Team,
        related_name='team_members',
        on_delete=CASCADE, null=False, db_column='team'
    )
    user = ForeignKey(
        User,
        related_name='user_memberships',
        on_delete=CASCADE, null=False, db_column='user'
    )

    def __str__(self):
        return str(self.id)
