from django.contrib import admin
from .models import Position, Resume, WorkExperience, Profile, Report

class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cpf', 'state', 'email', 'phone']
    search_fields = ["name", "phone"]


admin.site.register(Position)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(WorkExperience)
admin.site.register(Profile)
admin.site.register(Report)
