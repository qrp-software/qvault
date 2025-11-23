from rest_framework import serializers
from teknopark.models import (
    TeknoparkUser,
    TeknoparkPDKSEntryLog,
    TeknoparkPDKSEntry,
    TeknoparkPDKSMonthlyReport,
)
from users.api.serializers import UserSerializer


class TeknoparkUserSerializer(serializers.ModelSerializer):
    """Teknopark user serializer"""
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeknoparkUser
        fields = [
            "id",
            "user",
            "is_active",
            "weekly_working_hours",
            "created_date",
            "modified_date",
        ]
        read_only_fields = ["id", "created_date", "modified_date"]


class TeknoparkPDKSEntryLogSerializer(serializers.ModelSerializer):
    """PDKS giriş log serializer"""

    teknopark_user = TeknoparkUserSerializer(read_only=True)
    log_type_display = serializers.CharField(
        source="get_log_type_display",
        read_only=True,
    )

    class Meta:
        model = TeknoparkPDKSEntryLog
        fields = [
            "id",
            "teknopark_user",
            "log_type",
            "log_type_display",
            "timestamp",
            "created_date",
            "modified_date",
        ]
        read_only_fields = ["id", "teknopark_user", "created_date", "modified_date"]

    def create(self, validated_data):
        # Teknopark kullanıcısını request'ten al
        user = self.context["request"].user
        try:
            teknopark_user = TeknoparkUser.objects.get(user=user)
        except TeknoparkUser.DoesNotExist:
            raise serializers.ValidationError("Teknopark kullanıcısı bulunamadı")
        validated_data["teknopark_user"] = teknopark_user

        return super().create(validated_data)


class TeknoparkPDKSEntrySerializer(serializers.ModelSerializer):
    """Daily attendance serializer"""

    teknopark_user = TeknoparkUserSerializer(read_only=True)

    class Meta:
        model = TeknoparkPDKSEntry
        fields = [
            "id",
            "teknopark_user",
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
            "teknopark_user",
            "total_hours",
            "entry_count",
            "first_entry",
            "last_exit",
            "created_date",
            "modified_date",
        ]


class TeknoparkPDKSMonthlyReportSerializer(serializers.ModelSerializer):
    """Monthly report serializer"""

    teknopark_user = TeknoparkUserSerializer(read_only=True)
    month_display = serializers.CharField(
        source="get_month_display",
        read_only=True,
    )

    class Meta:
        model = TeknoparkPDKSMonthlyReport
        fields = [
            "id",
            "teknopark_user",
            "year",
            "month",
            "month_display",
            "total_hours",
            "required_hours",
            "remaining_hours",
            "total_days",
            "average_hours_per_day",
            "last_calculated",
        ]
        read_only_fields = [
            "id",
            "teknopark_user",
            "total_hours",
            "required_hours",
            "remaining_hours",
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
        # Teknopark kullanıcısını request'ten al
        user = self.context["request"].user
        try:
            teknopark_user = TeknoparkUser.objects.get(user=user)
        except TeknoparkUser.DoesNotExist:
            raise serializers.ValidationError("Teknopark kullanıcısı bulunamadı")
        validated_data["teknopark_user"] = teknopark_user

        return super().create(validated_data)

