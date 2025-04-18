from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied, NotFound
from typing import Optional
from .models import Invite
from teams.models import Team


def verify_team_leader(team: Optional[Team], auth_user: User):
    if team is None:
        raise NotFound({'message': 'Invalid team_id'})

    # Only team leader should be able to deal with invites
    if auth_user.id != team.leader.id:
        raise PermissionDenied({'message': 'Forbidden'})


def verify_invite(invite: Optional[Invite]) -> Invite:
    if invite is None:
        raise NotFound({'message': 'Invalid invite'})

    return invite
