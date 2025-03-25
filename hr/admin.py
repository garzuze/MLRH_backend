from django import forms
from django.contrib import admin
from .models import Position, Resume, WorkExperience, Profile, Report

class WorkExperienceliner(admin.StackedInline):
    model = WorkExperience


class ResumeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "cpf", "state", "email", "phone"]
    search_fields = ["name", "phone"]
    inlines = [WorkExperienceliner]


class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["id", "title"]


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "client_contact",
        "position",
        "status",
        "estimated_delivery",
    ]
    search_fields = [
        "client",
        "position",
    ]

admin.site.register(Position, PositionAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(WorkExperience)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Report)
