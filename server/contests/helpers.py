from rest_framework.exceptions import NotFound
from common.exceptions import BadRequest
from contests.models import Contest, TeamContestRegistration
import textwrap
import environ

env = environ.Env()
environ.Env.read_env()


def get_contest(contest_id: int):
    if not contest_id:
        raise BadRequest(message='No contest_id provided.')

    contest = Contest.objects.filter(id=contest_id).first()

    if not contest:
        raise NotFound({'message': 'Invalid contest id'})

    return contest


def get_team_reg(team_id: str, contest_id: int):
    if not team_id:
        raise BadRequest(message='No team_id provided.')

    if not contest_id:
        raise BadRequest(message='No contest_id provided.')

    team_reg = TeamContestRegistration.objects.filter(
        team=team_id,
        contest=contest_id
    ).first()

    return team_reg


def get_contest_registration_email_message(user_first_name, contest_name, club_name):
    """
    Generate email message for contest registration confirmation.
    """
    return textwrap.dedent(f'''\
        Hi {user_first_name},

        Thank you for registering for {contest_name} organized by {club_name} at Moksha IX – 2025.

        Your registration has been successfully recorded in our system. We're excited to have you participate!

        Important Details:
        - Contest: {contest_name}
        - Organizer: {club_name}

        Please make sure to check the contest guidelines and schedule on our website or mobile app.
        If you have any questions or need assistance, feel free to contact us at {env('EMAIL_HOST_USER')}.

        We look forward to seeing your participation!

        Best regards,
        Moksha IX Tech Team
        National Institute of Technology, Agartala
    ''')


def get_team_contest_registration_email_message(user_first_name, team_name, contest_name, club_name):
    """
    Generate email message for team contest registration confirmation.
    """
    return textwrap.dedent(f'''\
        Hi {user_first_name},

        Your team "{team_name}" has been successfully registered for {contest_name} organized by {club_name} at Moksha IX – 2025.

        Your team's registration has been recorded in our system. We're excited to have your team participate!

        Important Details:
        - Contest: {contest_name}
        - Organizer: {club_name}
        - Team: {team_name}

        Please make sure to check the contest guidelines and schedule on our website or mobile app.
        If you have any questions or need assistance, feel free to contact us at {env('EMAIL_HOST_USER')}.

        We look forward to seeing your team's participation!

        Best regards,
        Moksha IX Tech Team
        National Institute of Technology, Agartala
    ''')
