from rest_framework.exceptions import NotFound
from common.exceptions import BadRequest
from contests.models import Contest, TeamContestRegistration


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
