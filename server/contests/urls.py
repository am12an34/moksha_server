from rest_framework.urls import path
from .views import *

urlpatterns = [
    path('/solo/registration', SoloContestRegistration.as_view()),
    path('/team/registration', TeamContestRegistration.as_view()),
    path('/<slug:club_slug>/<slug:contest_slug>', GetContestRegistrations.as_view()),
]
