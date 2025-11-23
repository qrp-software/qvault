from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from teknopark.models import (
    TeknoparkUser,
    TeknoparkPDKSEntryLog,
    TeknoparkPDKSEntry,
    TeknoparkPDKSMonthlyReport,
)
from .serializers import (
    TeknoparkPDKSEntryLogSerializer,
    TeknoparkPDKSEntrySerializer,
    TeknoparkPDKSMonthlyReportSerializer,
    TeknoparkPDKSEntryLogCreateSerializer,
)
from .filters import (
    TeknoparkPDKSEntryLogFilter,
    TeknoparkPDKSEntryFilter,
    TeknoparkPDKSMonthlyReportFilter,
)
from teknopark.enums import MonthChoices


class TeknoparkPDKSEntryLogViewSet(viewsets.ModelViewSet):
    """ViewSet for attendance logs"""

    serializer_class = TeknoparkPDKSEntryLogSerializer
    filterset_class = TeknoparkPDKSEntryLogFilter
    ordering = ["-timestamp"]

    def get_queryset(self):
        # Kullanıcı sadece kendi loglarını görebilir
        try:
            teknopark_user = TeknoparkUser.objects.get(user=self.request.user)
            return TeknoparkPDKSEntryLog.objects.filter(teknopark_user=teknopark_user)
        except TeknoparkUser.DoesNotExist:
            return TeknoparkPDKSEntryLog.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return TeknoparkPDKSEntryLogCreateSerializer
        return TeknoparkPDKSEntryLogSerializer

    @action(detail=False, methods=["get"])
    def today(self, request):
        """Bugünkü logları getir"""
        today = timezone.now().date()
        start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        end_of_day = start_of_day + timedelta(days=1)

        logs = self.get_queryset().filter(
            timestamp__gte=start_of_day,
            timestamp__lt=end_of_day,
        )

        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)


class TeknoparkPDKSEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for daily attendance (read-only)"""

    serializer_class = TeknoparkPDKSEntrySerializer
    filterset_class = TeknoparkPDKSEntryFilter
    ordering = ["-date"]

    def get_queryset(self):
        # Kullanıcı sadece kendi günlük yoklamalarını görebilir
        try:
            teknopark_user = TeknoparkUser.objects.get(user=self.request.user)
            return TeknoparkPDKSEntry.objects.filter(teknopark_user=teknopark_user)
        except TeknoparkUser.DoesNotExist:
            return TeknoparkPDKSEntry.objects.none()

    @action(detail=False, methods=["get"])
    def today(self, request):
        """Bugünkü yoklamayı getir"""
        try:
            teknopark_user = TeknoparkUser.objects.get(user=request.user)
        except TeknoparkUser.DoesNotExist:
            return Response(
                {"error": "Teknopark kullanıcısı bulunamadı"}, status=404
            )
        
        today = timezone.now().date()
        pdks_entry = TeknoparkPDKSEntry.objects.filter(
            teknopark_user=teknopark_user,
            date=today,
        ).first()

        if not pdks_entry:
            # Eğer bugün için kayıt yoksa oluştur ve hesapla
            pdks_entry = TeknoparkPDKSEntry.objects.create(
                teknopark_user=teknopark_user,
                date=today,
            )
            pdks_entry.calculate_total_hours()

        serializer = self.get_serializer(pdks_entry)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Günlük yoklama özeti"""
        queryset = self.get_queryset()

        # Özet istatistikler
        total_hours = queryset.aggregate(total=Sum("total_hours"))["total"] or 0.00
        total_days = queryset.count()
        average_hours = round(total_hours / total_days, 2) if total_days > 0 else 0.00

        return Response(
            {
                "total_hours": float(total_hours),
                "total_days": total_days,
                "average_hours_per_day": average_hours,
            }
        )


class TeknoparkPDKSMonthlyReportViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for monthly reports (read-only)"""

    serializer_class = TeknoparkPDKSMonthlyReportSerializer
    filterset_class = TeknoparkPDKSMonthlyReportFilter
    ordering = ["-year", "-month"]

    def get_queryset(self):
        # Kullanıcı sadece kendi aylık raporlarını görebilir
        try:
            teknopark_user = TeknoparkUser.objects.get(user=self.request.user)
            return TeknoparkPDKSMonthlyReport.objects.filter(teknopark_user=teknopark_user)
        except TeknoparkUser.DoesNotExist:
            return TeknoparkPDKSMonthlyReport.objects.none()

    @action(detail=False, methods=["get"])
    def current_month(self, request):
        """Bu ayın raporunu getir veya oluştur"""
        try:
            teknopark_user = TeknoparkUser.objects.get(user=request.user)
        except TeknoparkUser.DoesNotExist:
            return Response(
                {"error": "Teknopark kullanıcısı bulunamadı"}, status=404
            )
        
        now = timezone.now()
        year = now.year
        month = now.month

        report = TeknoparkPDKSMonthlyReport.objects.filter(
            teknopark_user=teknopark_user,
            year=year,
            month=month,
        ).first()

        if not report:
            # Eğer bu ay için rapor yoksa oluştur ve hesapla
            report = TeknoparkPDKSMonthlyReport.objects.create(
                teknopark_user=teknopark_user,
                year=year,
                month=month,
            )
            report.calculate()

        serializer = self.get_serializer(report)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def create_report(self, request):
        """Belirtilen ayın raporunu getir veya oluştur ve hesapla"""
        # Query parametrelerinden year ve month al, yoksa şu anki ayı kullan
        now = timezone.now()
        year = request.query_params.get("year") or now.year
        month = request.query_params.get("month") or now.month

        try:
            year = int(year)
            month = int(month)

            # Ay değerinin geçerli olduğunu kontrol et
            if month not in MonthChoices.values:
                return Response(
                    {"error": "Ay değeri 1-12 arasında olmalıdır"}, status=400
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "Year ve month parametreleri geçerli sayılar olmalıdır"},
                status=400,
            )

        try:
            teknopark_user = TeknoparkUser.objects.get(user=request.user)
        except TeknoparkUser.DoesNotExist:
            return Response(
                {"error": "Teknopark kullanıcısı bulunamadı"}, status=404
            )

        # Raporu getir veya oluştur, sonra hesapla
        report, created = TeknoparkPDKSMonthlyReport.objects.get_or_create(
            teknopark_user=teknopark_user,
            year=year,
            month=month,
        )

        # Her durumda hesapla (kayıt varsa üzerine yaz)
        report.calculate()

        serializer = self.get_serializer(report)
        return Response(serializer.data)
