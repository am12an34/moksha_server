from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import CharField
from .serializers import UserSerializer
from common.decorators import login_required
from invites.serializers import InviteSerializer
from teams.serializers import TeamSerializer, TeamMemberSerializer
from contests.serializers import ContestSerializer, SoloContestRegistrationSerializer, TeamContestRegistrationSerializer, TeamContestUserRegistrationSerializer


@method_decorator(login_required, name="dispatch")
class AuthUser(APIView):
    def get(self, request):
        return Response(data={
            'id': request.user.id,
            'tag': request.user.profile.tag,
            'avatar_idx': request.user.profile.avatar_idx,
            'institution': request.user.profile.institution,
            'phone_no': request.user.profile.phone_no,
            'email': request.user.email,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })

    def patch(self, request):
        user = request.user
        is_updated = False

        if request.data.get('first_name', False):
            user.first_name = request.data['first_name']
            is_updated = True

        if request.data.get('last_name', False):
            user.last_name = request.data['last_name']
            is_updated = True

        if request.data.get('institution', False):
            user.profile.institution = request.data['institution']
            is_updated = True

        if request.data.get('phone_no', False):
            user.profile.phone_no = request.data['phone_no']
            is_updated = True

        if is_updated:
            user.save()
            user.profile.save()

        return Response(data={'message': 'Your information has been updated'})


@method_decorator(login_required, name="dispatch")
class Users(APIView):
    def get(self, request):
        username = request.GET.get('username', None)
        limit = request.GET.get('limit', 10)

        if username is None:
            return Response({'data': []}, status=200)

        users = User.objects.filter(
            Q(username__icontains=username)
            & ~Q(user_id=request.user.user_id)
        ).all()[0:limit]

        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data)


@method_decorator(login_required, name="dispatch")
class AuthUserCreatedTeam(APIView):
    def get(self, request):
        created_team = request.user.created_team.first()

        if created_team:
            serializer = TeamSerializer(created_team)
            return Response(data=serializer.data)

        return Response(data=None)


@method_decorator(login_required, name="dispatch")
class AuthUserJoinedTeams(APIView):
    def get(self, request):
        created_team = request.user.created_team.first()
        user_memberships = request.user.user_memberships.filter(
            ~Q(team__team_id=created_team)).all()

        serializer = TeamMemberSerializer(
            user_memberships,
            many=True,
            read_only=True,
            fields={'team': TeamSerializer()}
        )
        return Response(data=serializer.data)


@method_decorator(login_required, name="dispatch")
class AuthUserReceivedTeamInvites(APIView):
    def get(self, request):
        received_invites = request.user.received_invites.all()

        serializer = InviteSerializer(
            received_invites,
            many=True,
            read_only=True,
            fields={'team': TeamSerializer(
                empty=True,
                fields={'team_id': CharField(), 'team_name': CharField()}
            )}
        )

        return Response(data=serializer.data)


@method_decorator(login_required, name="dispatch")
class AuthUserSoloContests(APIView):
    def get(self, request):
        solo_contest_regs = request.user.registered_solo_contests.only(
            'contest').all()

        serializer = SoloContestRegistrationSerializer(
            solo_contest_regs,
            read_only=True,
            many=True,
            fields={'contest': ContestSerializer(read_only=True)}
        )
        return Response(data=serializer.data)


@method_decorator(login_required, name="dispatch")
class AuthUserTeamContests(APIView):
    def get(self, request):
        contest_id = request.GET.get('contest_id', None)

        # All registered contest of auth user's created team
        if contest_id is None:
            team_contest_regs = request.user.team_contest_registrations.only(
                'team_contest_registration').all()

            serializer = TeamContestUserRegistrationSerializer(
                team_contest_regs,
                read_only=True,
                empty=True,
                many=True,
                fields={
                    'team_contest_registration': TeamContestRegistrationSerializer(
                        fields={
                            'contest': ContestSerializer(),
                            'team': TeamSerializer(
                                empty=True,
                                fields={'team_id': CharField(
                                ), 'team_name': CharField()}
                            )
                        }
                    )
                }
            )

            return Response(data=serializer.data)

        # A particular contest registration of auth user's created team
        team_contest_reg = request.user.team_contest_registrations.only(
            'team_contest_registration').filter(team_contest_registration__contest=contest_id).first()

        if team_contest_reg is None:
            return Response({'data': None, 'message': 'No registration found'})

        serializer = TeamContestUserRegistrationSerializer(
            team_contest_reg,
            read_only=True,
            empty=True,
            fields={
                'team_contest_registration': TeamContestRegistrationSerializer(
                    read_only=True,
                    fields={
                        'team': TeamSerializer(read_only=True),
                        'registered_members': TeamContestUserRegistrationSerializer(many=True)
                    }
                )
            }
        )
        return Response(data=serializer.data)
