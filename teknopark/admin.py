from django.contrib import admin
from django.utils.html import format_html
from .models import (
    TeknoparkUser,
    TeknoparkPDKSEntryLog,
    TeknoparkPDKSEntry,
    TeknoparkPDKSMonthlyReport,
)


@admin.register(TeknoparkUser)
class TeknoparkUserAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "is_active",
        "weekly_working_hours",
        "created_date",
        "modified_date",
    ]
    list_filter = ["is_active", "created_date"]
    search_fields = ["user__username", "user__email"]
    readonly_fields = ["created_date", "modified_date"]
    ordering = ["-created_date"]

    fieldsets = (
        (
            "Temel Bilgiler",
            {
                "fields": (
                    "user",
                    "is_active",
                    "weekly_working_hours",
                    "weekly_working_days",
                ),
            },
        ),
        (
            "Sistem Bilgileri",
            {
                "fields": ("created_date", "modified_date"),
            },
        ),
    )


@admin.register(TeknoparkPDKSEntryLog)
class TeknoparkPDKSEntryLogAdmin(admin.ModelAdmin):
    list_display = ["teknopark_user", "log_type_display", "timestamp", "created_date"]
    list_filter = ["log_type", "timestamp", "created_date"]
    search_fields = ["teknopark_user__user__username", "teknopark_user__user__email"]
    readonly_fields = ["created_date", "modified_date"]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    fieldsets = (
        (
            "Temel Bilgiler",
            {
                "fields": ("teknopark_user", "log_type", "timestamp"),
            },
        ),
        (
            "Sistem Bilgileri",
            {
                "fields": ("created_date", "modified_date"),
            },
        ),
    )

    def log_type_display(self, obj):
        return obj.get_log_type_display()

    log_type_display.short_description = "Log Tipi"


@admin.register(TeknoparkPDKSEntry)
class TeknoparkPDKSEntryAdmin(admin.ModelAdmin):
    list_display = [
        "teknopark_user",
        "date",
        "total_hours",
        "entry_count",
        "first_entry",
        "last_exit",
    ]
    list_filter = ["date", "created_date"]
    search_fields = ["teknopark_user__user__username", "teknopark_user__user__email"]
    readonly_fields = [
        "total_hours",
        "entry_count",
        "first_entry",
        "last_exit",
        "created_date",
        "modified_date",
    ]
    date_hierarchy = "date"
    ordering = ["-date"]

    fieldsets = (
        (
            "Temel Bilgiler",
            {
                "fields": ("teknopark_user", "date"),
            },
        ),
        (
            "Yoklama Bilgileri",
            {
                "fields": (
                    "total_hours",
                    "entry_count",
                    "first_entry",
                    "last_exit",
                ),
            },
        ),
        (
            "Sistem Bilgileri",
            {
                "fields": ("created_date", "modified_date"),
            },
        ),
    )

    actions = ["recalculate_attendance"]

    def recalculate_attendance(self, request, queryset):
        """Seçili günlük yoklamaları yeniden hesapla"""
        count = 0
        for attendance in queryset:
            attendance.calculate_total_hours()
            count += 1
        self.message_user(request, f"{count} günlük yoklama yeniden hesaplandı.")

    recalculate_attendance.short_description = "Seçili yoklamaları yeniden hesapla"


@admin.register(TeknoparkPDKSMonthlyReport)
class TeknoparkPDKSMonthlyReportAdmin(admin.ModelAdmin):
    list_display = [
        "teknopark_user",
        "year",
        "month_display",
        "total_hours",
        "required_hours",
        "remaining_hours",
        "total_days",
        "average_hours_per_day",
        "last_calculated",
    ]
    list_filter = ["year", "month", "last_calculated"]
    search_fields = ["teknopark_user__user__username", "teknopark_user__user__email"]
    readonly_fields = [
        "total_hours",
        "required_hours",
        "remaining_hours",
        "total_days",
        "average_hours_per_day",
        "last_calculated",
    ]
    ordering = ["-year", "-month"]

    fieldsets = (
        (
            "Temel Bilgiler",
            {
                "fields": ("teknopark_user", "year", "month"),
            },
        ),
        (
            "Rapor Bilgileri",
            {
                "fields": (
                    "total_hours",
                    "required_hours",
                    "remaining_hours",
                    "total_days",
                    "average_hours_per_day",
                ),
            },
        ),
        (
            "Sistem Bilgileri",
            {
                "fields": ("last_calculated",),
            },
        ),
    )

    actions = ["recalculate_reports"]

    def month_display(self, obj):
        return obj.get_month_display()

    month_display.short_description = "Ay"

    def recalculate_reports(self, request, queryset):
        """Seçili aylık raporları yeniden hesapla"""
        count = 0
        for report in queryset:
            report.calculate()
            count += 1
        self.message_user(request, f"{count} aylık rapor yeniden hesaplandı.")

    recalculate_reports.short_description = "Seçili raporları yeniden hesapla"
