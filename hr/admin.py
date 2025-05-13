from django import forms
from django.contrib import admin
from .models import Position, Resume, WorkExperience, Profile, Report


class WorkExperienceInliner(admin.StackedInline):
    model = WorkExperience
    extra = 0
    ordering = ("-start_date", )

class ReportInliner(admin.StackedInline):
    model = Report
    extra = 0


class ResumeAdmin(admin.ModelAdmin):
    def updated(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y")

    updated.admin_order_field = "updated_at"
    updated.short_description = "Atualizado em"

    list_display = [
        "id",
        "name",
        "phone",
        "expected_salary",
        "neighborhood",
        "city",
        "age",
        "position",
        "updated",
    ]

    search_fields = ["name", "phone", "desired_positions__title"]
    autocomplete_fields = ["desired_positions"]
    inlines = [WorkExperienceInliner]


class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["id", "title"]


class ProfileAdmin(admin.ModelAdmin):
    def created(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")

    created.admin_order_field = "created_at"
    created.short_description = "Criado em"
    list_display = [
        "client__trade_name",
        "client_contact__name",
        "position",
        "status",
        "created",
        "reports_list"
    ]

    search_fields = [
        "client__trade_name",
        "position__title",
    ]

    list_filter = ["status"]

    inlines = [ReportInliner]


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
