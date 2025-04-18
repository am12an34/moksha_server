from rest_framework.urls import path
from .views import *

urlpatterns = [
    path('', CreateTeam.as_view()),
    path('/<slug:team_id>', GetTeam.as_view()),
    path('/<slug:team_id>/members', GetTeamMembers.as_view()),
    path(
        '/<slug:team_id>/members/<int:contest_id>',
        GetContestRegisteredTeamMembers.as_view()
    ),
    path(
        '/<slug:team_id>/search/uninvited-users',
        GetUninvitedUsers().as_view()
    ),
    path(
        '/<slug:team_id>/registered-contests',
        GetRegisteredTeamContests().as_view()
    ),
    path('/<slug:team_id>/pending-invites', GetPendingInvites.as_view())
]
