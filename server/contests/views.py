from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from common.decorators import login_required, body
from common.responses import NoContentResponse
from common.exceptions import BadRequest, Conflict
from contests.helpers import get_contest, get_team_reg, get_contest_registration_email_message, get_team_contest_registration_email_message
from users.serializers import AuthUserSerializer
from teams.helpers import get_team
from teams.serializers import TeamSerializer
from .models import SoloContestRegistration as SoloContestRegistrationModel, TeamContestRegistration as TeamContestRegistrationModel, TeamContestUserRegistration
from .serializers import SoloContestRegistrationSerializer, TeamContestRegistrationSerializer, TeamContestUserRegistrationSerializer
import environ

env = environ.Env()
environ.Env.read_env()


@method_decorator(login_required, name="dispatch")
class SoloContestRegistration(APIView):
    def get(self, request):
        contest_id = request.GET['contest_id']
        contest = get_contest(contest_id)

        solo_reg = SoloContestRegistrationModel.objects.filter(
            user=request.user,
            contest=contest
        ).first()

        if not solo_reg:
            return Response(data=None)

        serializer = SoloContestRegistrationSerializer(solo_reg)
        return Response(data=serializer.data)

    @body({'contest_id'})
    def post(self, request):
        contest_id = request.data['contest_id']
        contest = get_contest(contest_id)

        solo_reg_exists = SoloContestRegistrationModel.objects.filter(
            user=request.user,
            contest=contest
        ).exists()

        if solo_reg_exists:
            raise Conflict(message='User already registered for the contest.')

        solo_reg = SoloContestRegistrationModel(
            user=request.user,
            contest=contest
        )
        solo_reg.save()

        # Send email notification for successful registration
        try:
            send_mail(
                subject=f'Moksha IX - Registration Confirmation for {contest.contest_slug}',
                message=get_contest_registration_email_message(
                    request.user.first_name,
                    contest.contest_slug,
                    contest.club_slug
                ),
                from_email=env('EMAIL_HOST_USER'),
                recipient_list=[request.user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't fail the registration process
            pass

        serializer = SoloContestRegistrationSerializer(solo_reg)
        return Response(data=serializer.data, status=201)

    @body({'solo_reg_id'})
    def delete(self, request):
        solo_reg_id = request.data['solo_reg_id']

        solo_reg = SoloContestRegistrationModel.objects.filter(
            id=solo_reg_id).first()

        if not solo_reg:
            raise NotFound({'message': 'No registration found.'})

        solo_reg.delete()
        return NoContentResponse()


@method_decorator(login_required, name="dispatch")
class TeamContestRegistration(APIView):
    def get(self, request):
        team_id = request.GET['team_id']
        contest_id = request.GET['contest_id']

        team_reg = get_team_reg(team_id, contest_id)

        if not team_reg:
            return Response(data=None)

        serializer = TeamContestRegistrationSerializer(
            team_reg,
            fields={'registered_members': TeamContestUserRegistrationSerializer(
                read_only=True,
                many=True
            )}
        )

        return Response(data=serializer.data)

    @body({'team_id', 'contest_id', 'selected_members'})
    def post(self, request):
        team_id = request.data['team_id']
        contest_id = request.data['contest_id']
        selected_members = request.data['selected_members']

        team_reg_exists = TeamContestRegistrationModel.objects.filter(
            team=team_id,
            contest=contest_id
        ).exists()

        if team_reg_exists:
            raise Conflict(message='Team already registered for the contest.')

        team = get_team(team_id)
        contest = get_contest(contest_id)

        team_reg = TeamContestRegistrationModel(team=team, contest=contest)
        team_reg.save()

        team_reg_members = []

        for member_id in selected_members:
            team_reg_members.append(TeamContestUserRegistration(
                team_contest_registration=team_reg,
                user=User.objects.get(id=member_id)
            ))

        TeamContestUserRegistration.objects.bulk_create(team_reg_members)

        team_reg = get_team_reg(team_id, contest_id)

        if team_reg is None:
            return Response({'data': None, 'message': 'No registration found.'})

        # Send email notifications to all team members
        try:
            # Get all user objects for the selected members
            member_users = User.objects.filter(id__in=selected_members).all()

            # Send emails to all team members
            for user in member_users:
                send_mail(
                    subject=f'Moksha IX - Team Registration Confirmation for {contest.contest_slug}',
                    message=get_team_contest_registration_email_message(
                        user.first_name,
                        team.team_name,
                        contest.contest_slug,
                        contest.club_slug
                    ),
                    from_email=env('EMAIL_HOST_USER'),
                    recipient_list=[user.email],
                    fail_silently=False,
                )
        except Exception as e:
            # Log the error but don't fail the registration process
            pass

        serializer = TeamContestRegistrationSerializer(
            team_reg,
            fields={'registered_members': TeamContestUserRegistrationSerializer(
                read_only=True,
                many=True
            )}
        )

        return Response(data=serializer.data, status=201)

    @body({'team_id', 'contest_id'})
    def delete(self, request):
        team_id = request.data['team_id']
        contest_id = request.data['contest_id']

        team_reg = get_team_reg(team_id, contest_id)

        if team_reg is None:
            raise NotFound({'message': 'No registration found.'})

        team_reg.delete()

        return NoContentResponse()


# This below api is meant for admin client only
# No role-based auth is implemented yet


class GetContestRegistrations(APIView):
    def get(self, request, club_slug, contest_slug):
        contest_type = request.GET.get('type', None)

        if (contest_type is None):
            raise BadRequest(message='No contest type specified')

        if contest_type == 'solo':
            data = SoloContestRegistrationModel.objects.filter(
                contest__club_slug=club_slug, contest__contest_slug=contest_slug).all()

            serializer = SoloContestRegistrationSerializer(
                data,
                many=True,
                empty=True,
                # AuthUserSerializer is used here to get email and phone for admin client
                fields={'user': AuthUserSerializer()}
            )

            return Response({'data': serializer.data})

        else:
            data = TeamContestRegistrationModel.objects.filter(
                contest__club_slug=club_slug, contest__contest_slug=contest_slug).all()

            serializer = TeamContestRegistrationSerializer(
                data,
                many=True,
                empty=True,
                fields={
                    'team': TeamSerializer(),
                    'registered_members': TeamContestUserRegistrationSerializer(
                        many=True,
                        # AuthUserSerializer is used here to get email and phone for admin client
                        fields={'user': AuthUserSerializer()}
                    )
                }
            )

            return Response({'data': serializer.data})
