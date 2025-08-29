from django.contrib import admin
from .models import Registration,TeamMember,Collaboration,Job

# Register your models here.
admin.site.register(Registration)
admin.site.register(TeamMember)
admin.site.register(Collaboration)
admin.site.register(Job)
