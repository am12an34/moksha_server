from common.exceptions import BadRequest, NotFound
from teams.models import Team


def get_team(team_id: str) -> Team:
    if not team_id:
        raise BadRequest(message='No team_id provided.')

    team = Team.objects.filter(team_id=team_id).first()

    if not team:
        raise NotFound(message='Invalid team id')

    return team
