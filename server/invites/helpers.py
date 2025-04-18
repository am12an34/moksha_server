from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied, NotFound
from typing import Optional
import textwrap
import environ
from .models import Invite
from teams.models import Team

env = environ.Env()
environ.Env.read_env()


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


def get_team_invitation_email_message(invited_user_first_name, team_name, leader_first_name, leader_last_name):
    """
    Generate email message for team invitation.
    """
    return textwrap.dedent(f'''\
        Hi {invited_user_first_name},

        You have been invited to join team "{team_name}" by {leader_first_name} {leader_last_name} for Moksha IX – 2025.

        To accept or reject this invitation, please log in to your Moksha account and check your team invitations.

        Joining a team will allow you to participate in team contests together. If you have any questions about this invitation,
        you can contact the team leader directly or reach out to us at {env('EMAIL_HOST_USER')}.

        Best regards,
        Moksha IX Tech Team
        National Institute of Technology, Agartala
    ''')
