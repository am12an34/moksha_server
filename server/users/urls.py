from rest_framework.urls import path
from .views import *

urlpatterns = [
    path('', Users.as_view()),
    path('/me', AuthUser.as_view()),
    path('/me/created-team', AuthUserCreatedTeam.as_view()),
    path('/me/joined-teams', AuthUserJoinedTeams.as_view()),
    path('/me/received-team-invites', AuthUserReceivedTeamInvites.as_view()),
    path('/me/registered-solo-contests', AuthUserSoloContests.as_view()),
    path('/me/registered-team-contests', AuthUserTeamContests.as_view()),
]
