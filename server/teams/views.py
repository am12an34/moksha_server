from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction, IntegrityError
from .helpers import get_team
from .models import Team, TeamMember
from .serializers import TeamSerializer
from common.decorators import login_required, body
from common.exceptions import BadRequest, Conflict, InternalServerError
from users.serializers import UserSerializer
from invites.helpers import verify_team_leader
from invites.models import Invite
from invites.serializers import InviteSerializer
from contests.helpers import get_contest
from contests.serializers import ContestSerializer, TeamContestRegistrationSerializer, TeamContestUserRegistrationSerializer
import secrets
import string


@method_decorator(login_required, name="dispatch")
class CreateTeam(APIView):
    @body({'team_name'})
    def post(self, request):
        team_name = request.data['team_name']

        try:
            with transaction.atomic():
                if Team.objects.filter(leader=request.user).exists():
                    raise Conflict(
                        message='A team is already created by the user.')

                if Team.objects.filter(team_name__iexact=team_name).exists():
                    raise Conflict(message='This team name is already taken.')

                team_id = generate_uid()

                while Team.objects.filter(team_id=team_id).exists():
                    team_id = generate_uid()

                new_team = Team(
                    team_id=team_id,
                    team_name=team_name,
                    leader=request.user
                )
                new_team.save()

                new_team_member = TeamMember(
                    team=new_team,
                    user=request.user
                )
                new_team_member.save()
        except IntegrityError:
            raise InternalServerError()

        return Response(data={'team_id': team_id}, status=201)


class GetTeam(APIView):
    def get(self, _, team_id):
        team = get_team(team_id)
        serializer = TeamSerializer(team)
        return Response(data=serializer.data)


class GetTeamMembers(APIView):
    def get(self, _, team_id):
        user_ids = TeamMember.objects.filter(
            team_id=team_id).values_list('user')
        users = User.objects.filter(id__in=user_ids)

        serializer = UserSerializer(users, many=True)

        return Response(data=serializer.data)


@method_decorator(login_required, name="dispatch")
class GetContestRegisteredTeamMembers(APIView):
    def get(self, _, team_id, contest_id):
        team = get_team(team_id)
        contest = get_contest(contest_id)

        team_members = team.team_members.values_list(
            'user__id',
            flat=True
        )
        registered_users_in_contest = contest.registered_teams.filter(
            registered_members__user__id__in=team_members
        ).values_list(
            'registered_members__user__id',
            flat=True
        ).all()

        return Response(data=registered_users_in_contest)


@method_decorator(login_required, name="dispatch")
class GetUninvitedUsers(APIView):
    def get(self, request, team_id):
        username = request.GET.get('username', None)
        limit = request.GET.get('limit', 10)

        if username is None:
            return Response(data=[])

        team_members = TeamMember.objects.filter(
            team=team_id).values_list('user', flat=True)

        pending_invites = Invite.objects.filter(
            Q(team=team_id)).values_list('user', flat=True)

        users = User.objects.filter(
            Q(username__icontains=username)
            & ~Q(id=request.user.id)
            & ~Q(id__in=team_members)
            & ~Q(id__in=pending_invites)
        ).all()[0:limit]

        data = []
        for user in users:
            serializer = UserSerializer(user)
            data.append(serializer.data)

        return Response(data=data)


@method_decorator(login_required, name="dispatch")
class GetRegisteredTeamContests(APIView):
    def get(self, request, team_id):
        team = get_team(team_id)

        contest_id = request.GET.get('contest_id', None)

        # All registered contests of a team
        if contest_id is None:
            team_contest_regs = team.registered_team_contests.all()  # type: ignore

            serializer = TeamContestRegistrationSerializer(
                team_contest_regs,
                read_only=True,
                many=True,
                fields={
                    'contest': ContestSerializer(),
                    'registered_members': TeamContestUserRegistrationSerializer(many=True)
                }
            )

            return Response(data=serializer.data)

        # A particular contest registration of a team
        team_contest_reg = team.registered_team_contests.filter(
            contest=contest_id).first()

        if team_contest_reg is None:
            return Response(data=None)

        serializer = TeamContestRegistrationSerializer(
            team_contest_reg,
            read_only=True,
            fields={
                'team': TeamSerializer(),
                'registered_members': TeamContestUserRegistrationSerializer(many=True)
            }
        )

        return Response(data=serializer.data)


@method_decorator(login_required, name="dispatch")
class GetPendingInvites(APIView):
    def get(self, request, team_id):
        team = Team.objects.filter(team_id=team_id).only('leader').first()

        verify_team_leader(team, request.user)

        pending_invites = team.pending_invites.all()

        serializer = InviteSerializer(
            pending_invites,
            many=True,
            fields={'user': UserSerializer()}
        )

        return Response(data=serializer.data)


def generate_uid(length=8):
    uid = ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                  for i in range(length))
    return 'T-' + uid
