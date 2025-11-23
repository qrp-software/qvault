import django_filters
from django.utils import timezone
from datetime import datetime
from teknopark.models import (
    TeknoparkPDKSEntryLog,
    TeknoparkPDKSEntry,
    TeknoparkPDKSMonthlyReport,
)


class TeknoparkPDKSEntryLogFilter(django_filters.FilterSet):
    """FilterSet for PDKS entry logs"""

    log_type = django_filters.CharFilter(field_name="log_type", lookup_expr="exact")
    date_from = django_filters.DateFilter(
        field_name="timestamp", lookup_expr="date__gte"
    )
    date_to = django_filters.DateFilter(field_name="timestamp", lookup_expr="date__lte")

    class Meta:
        model = TeknoparkPDKSEntryLog
        fields = ["log_type"]


class TeknoparkPDKSEntryFilter(django_filters.FilterSet):
    """FilterSet for daily PDKS entries"""

    date_from = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = TeknoparkPDKSEntry
        fields = []


class TeknoparkPDKSMonthlyReportFilter(django_filters.FilterSet):
    """FilterSet for monthly PDKS reports"""

    year = django_filters.NumberFilter(field_name="year", lookup_expr="exact")
    month = django_filters.NumberFilter(field_name="month", lookup_expr="exact")

    class Meta:
        model = TeknoparkPDKSMonthlyReport
        fields = ["year", "month"]

