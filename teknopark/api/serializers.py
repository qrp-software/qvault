from rest_framework import serializers
from teknopark.models import (
    TeknoparkPDKSEntryLog,
    TeknoparkPDKSEntry,
    TeknoparkPDKSMonthlyReport,
)
from users.api.serializers import UserSerializer


class TeknoparkPDKSEntryLogSerializer(serializers.ModelSerializer):
    """PDKS giriş log serializer"""

    user = UserSerializer(read_only=True)
    log_type_display = serializers.CharField(
        source="get_log_type_display",
        read_only=True,
    )

    class Meta:
        model = TeknoparkPDKSEntryLog
        fields = [
            "id",
            "user",
            "log_type",
            "log_type_display",
            "timestamp",
            "created_date",
            "modified_date",
        ]
        read_only_fields = ["id", "user", "created_date", "modified_date"]

    def create(self, validated_data):
        # Kullanıcıyı request'ten al
        user = self.context["request"].user
        validated_data["user"] = user

        return super().create(validated_data)


class TeknoparkPDKSEntrySerializer(serializers.ModelSerializer):
    """Daily attendance serializer"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = TeknoparkPDKSEntry
        fields = [
            "id",
            "user",
            "date",
            "total_hours",
            "entry_count",
            "first_entry",
            "last_exit",
            "created_date",
            "modified_date",
        ]
        read_only_fields = [
            "id",
            "user",
            "total_hours",
            "entry_count",
            "first_entry",
            "last_exit",
            "created_date",
            "modified_date",
        ]


class TeknoparkPDKSMonthlyReportSerializer(serializers.ModelSerializer):
    """Monthly report serializer"""

    user = UserSerializer(read_only=True)
    month_display = serializers.CharField(
        source="get_month_display",
        read_only=True,
    )

    class Meta:
        model = TeknoparkPDKSMonthlyReport
        fields = [
            "id",
            "user",
            "year",
            "month",
            "month_display",
            "total_hours",
            "total_days",
            "average_hours_per_day",
            "last_calculated",
        ]
        read_only_fields = [
            "id",
            "user",
            "total_hours",
            "total_days",
            "average_hours_per_day",
            "last_calculated",
        ]


class TeknoparkPDKSEntryLogCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating attendance logs from mobile app"""

    class Meta:
        model = TeknoparkPDKSEntryLog
        fields = ["log_type", "timestamp"]

    def create(self, validated_data):
        # Kullanıcıyı request'ten al
        user = self.context["request"].user
        validated_data["user"] = user

        return super().create(validated_data)

