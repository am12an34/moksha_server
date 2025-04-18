# from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin', admin.site.urls),
    path('api/auth', include('users_auth.urls')),
    path('api/users', include('users.urls')),
    path('api/teams', include('teams.urls')),
    path('api/contests', include('contests.urls')),
    path('api/invites', include('invites.urls')),
]
