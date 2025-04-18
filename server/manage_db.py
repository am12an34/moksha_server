import os
import django
import argparse
import sys

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from teams.models import Team, TeamMember
from contests.models import Contest, SoloContestRegistration, TeamContestRegistration
from invites.models import Invite

def list_users():
    """List all users in the database"""
    users = User.objects.all()

    if not users:
        print("No users found in the database.")
        return

    print(f"Found {users.count()} users:")
    for user in users:
        try:
            profile = user.profile
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Tag: {profile.tag}")
        except Profile.DoesNotExist:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, No profile")

def list_teams():
    """List all teams in the database"""
    teams = Team.objects.all()

    if not teams:
        print("No teams found in the database.")
        return

    print(f"Found {teams.count()} teams:")
    for team in teams:
        print(f"ID: {team.team_id}, Name: {team.team_name}, Leader: {team.leader.username}")

        members = TeamMember.objects.filter(team=team)
        print(f"  Members ({members.count()}):")
        for member in members:
            print(f"  - {member.user.username}")

def list_contests():
    """List all contests in the database"""
    contests = Contest.objects.all()

    if not contests:
        print("No contests found in the database.")
        return

    print(f"Found {contests.count()} contests:")
    for contest in contests:
        print(f"ID: {contest.id}, Contest Slug: {contest.contest_slug}, Club Slug: {contest.club_slug}, Is Solo: {contest.is_solo}")

        solo_regs = SoloContestRegistration.objects.filter(contest=contest)
        team_regs = TeamContestRegistration.objects.filter(contest=contest)

        print(f"  Solo Registrations: {solo_regs.count()}")
        print(f"  Team Registrations: {team_regs.count()}")

def list_invites():
    """List all invites in the database"""
    invites = Invite.objects.all()

    if not invites:
        print("No invites found in the database.")
        return

    print(f"Found {invites.count()} invites:")
    for invite in invites:
        print(f"ID: {invite.id}, Team: {invite.team.team_name}, User: {invite.user.username}")

def create_test_data():
    """Create test data in the database"""
    # Create a test user
    try:
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        # Create a profile for the user
        Profile.objects.create(
            user=user,
            tag="MOK-testuser",
            avatar_idx=1,
            institution="Test Institution",
            phone_no="1234567890"
        )

        print(f"Created test user: {user.username}")
    except Exception as e:
        print(f"Error creating test user: {str(e)}")

    # Create a test contest
    try:
        contest = Contest.objects.create(
            contest_slug="test-contest",
            club_slug="test-club",
            is_solo=False
        )

        print(f"Created test contest: {contest.contest_slug}")
    except Exception as e:
        print(f"Error creating test contest: {str(e)}")

def reset_database():
    """Reset the database by deleting all data"""
    # Ask for confirmation
    confirm = input("Are you sure you want to reset the database? This will delete all data. (y/n): ")

    if confirm.lower() != 'y':
        print("Database reset cancelled.")
        return

    # Delete all data
    Invite.objects.all().delete()
    TeamContestRegistration.objects.all().delete()
    SoloContestRegistration.objects.all().delete()
    Contest.objects.all().delete()
    TeamMember.objects.all().delete()
    Team.objects.all().delete()
    User.objects.all().delete()

    print("Database reset complete.")

def main():
    parser = argparse.ArgumentParser(description="Manage the Moksha database")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List users command
    subparsers.add_parser("list-users", help="List all users in the database")

    # List teams command
    subparsers.add_parser("list-teams", help="List all teams in the database")

    # List contests command
    subparsers.add_parser("list-contests", help="List all contests in the database")

    # List invites command
    subparsers.add_parser("list-invites", help="List all invites in the database")

    # Create test data command
    subparsers.add_parser("create-test-data", help="Create test data in the database")

    # Reset database command
    subparsers.add_parser("reset", help="Reset the database by deleting all data")

    args = parser.parse_args()

    if args.command == "list-users":
        list_users()
    elif args.command == "list-teams":
        list_teams()
    elif args.command == "list-contests":
        list_contests()
    elif args.command == "list-invites":
        list_invites()
    elif args.command == "create-test-data":
        create_test_data()
    elif args.command == "reset":
        reset_database()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
