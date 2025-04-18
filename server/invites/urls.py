from django.urls import path
from .views import *

urlpatterns = [
    path('', BaseEndpoint.as_view()),
    path('/<int:invite_id>/accept', AcceptInvite.as_view()),
    path('/<int:invite_id>/reject', RejectInvite.as_view()),
]
