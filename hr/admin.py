from django import forms
from django.contrib import admin
from .models import Position, Resume, WorkExperience, Profile, Report


class WorkExperienceliner(admin.StackedInline):
    model = WorkExperience
    extra = 0


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


class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = [
        "resume__name",
        "position_title",
        "company_name",
    ]
    search_fields = [
        "resume__name",
        "company_name",
        "position_title",
    ]
    ordering = ["resume__name"]
    list_filter = ("resume",)


class ReportAdmin(admin.ModelAdmin):
    list_display = [
        "profile__position__title",
        "profile__client",
        "resume__name",
        "agreed_salary",
    ]
    ordering = ["profile__position__title"]
    search_fields = [
        "profile__position__title",
        "profile__client",
        "resume__name",
    ]


admin.site.register(Position, PositionAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Report, ReportAdmin)
