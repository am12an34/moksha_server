from django.contrib import admin
from .models import Contest, SoloContestRegistration, TeamContestRegistration, TeamContestUserRegistration

# Register your models here.
admin.site.register(Contest)
admin.site.register(SoloContestRegistration)
admin.site.register(TeamContestRegistration)
admin.site.register(TeamContestUserRegistration)
