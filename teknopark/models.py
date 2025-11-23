from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from utils.models import StarterModel
from users.models import User
from teknopark.enums import PDKSLogType, MonthChoices


class TeknoparkPDKSEntryLog(StarterModel):
    """
    PDKS giriş logları
    Her giriş işlemi için ayrı kayıt tutulur
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pdkse_entry_logs",
        verbose_name="Kullanıcı",
    )
    log_type = models.CharField(
        max_length=10,
        choices=PDKSLogType.choices,
        verbose_name="PDKS Log Tipi",
    )
    timestamp = models.DateTimeField(
        verbose_name="Zaman",
        help_text="Giriş veya çıkış zamanı",
        default=timezone.now,
    )

    class Meta:
        verbose_name = "PDKS Giriş Logu"
        verbose_name_plural = "PDKS Giriş Logları"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["user", "log_type", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_daily_attendance()

    def _update_daily_attendance(self):
        """Günlük toplam süreyi hesapla ve güncelle"""
        date = self.timestamp.date()
        daily_attendance, created = TeknoparkPDKSEntry.objects.get_or_create(
            user=self.user,
            date=date,
        )
        daily_attendance.calculate_total_hours()


class TeknoparkPDKSEntry(StarterModel):
    """
    Kullanıcıların günlük toplam PDKS süreleri
    Her gün için bir kayıt tutulur ve otomatik hesaplanır
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pdks_entries",
        verbose_name="Kullanıcı",
    )
    date = models.DateField(
        verbose_name="Tarih",
        db_index=True,
    )
    total_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Toplam Süre (Saat)",
        help_text="O gün teknopark'ta geçirilen toplam süre",
    )
    entry_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Giriş Sayısı",
    )
    first_entry = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="İlk Giriş",
    )
    last_exit = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Son Çıkış",
    )

    class Meta:
        verbose_name = "Günlük Yoklama"
        verbose_name_plural = "Günlük Yoklamalar"
        unique_together = ("user", "date")
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.total_hours} saat"

    def calculate_total_hours(self):
        """Günlük toplam süreyi loglardan hesapla"""
        # O günün loglarını al
        start_of_day = timezone.make_aware(
            datetime.combine(self.date, datetime.min.time())
        )
        end_of_day = start_of_day + timedelta(days=1)

        logs = TeknoparkPDKSEntryLog.objects.filter(
            user=self.user,
            timestamp__gte=start_of_day,
            timestamp__lt=end_of_day,
        ).order_by("timestamp")

        # Giriş-çıkış çiftlerini hesapla
        total_seconds = 0
        entry_count = 0
        first_entry = None
        last_exit = None

        entry_time = None
        for log in logs:
            if log.log_type == "entry":
                entry_time = log.timestamp
                entry_count += 1
                if first_entry is None:
                    first_entry = log.timestamp
            elif log.log_type == "exit" and entry_time is not None:
                # Çıkış zamanından giriş zamanını çıkar
                duration = log.timestamp - entry_time
                total_seconds += duration.total_seconds()
                last_exit = log.timestamp
                entry_time = None

        # Eğer giriş yapılmış ama çıkış yapılmamışsa, şu anki zamana kadar say
        if entry_time is not None:
            duration = timezone.now() - entry_time
            total_seconds += duration.total_seconds()

        # Saate çevir (ondalıklı)
        self.total_hours = round(total_seconds / 3600, 2)
        self.entry_count = entry_count
        self.first_entry = first_entry
        self.last_exit = last_exit
        self.save(
            update_fields=["total_hours", "entry_count", "first_entry", "last_exit"]
        )


class TeknoparkPDKSMonthlyReport(models.Model):
    """
    Aylık raporlar için özet veri
    Performans için önceden hesaplanmış veriler
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pdks_monthly_reports",
        verbose_name="Kullanıcı",
    )
    year = models.PositiveIntegerField(verbose_name="Yıl")
    month = models.PositiveIntegerField(
        verbose_name="Ay",
        choices=MonthChoices.choices,
    )
    total_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name="Toplam Süre (Saat)",
    )
    total_days = models.PositiveIntegerField(
        default=0,
        verbose_name="Toplam Gün Sayısı",
    )
    average_hours_per_day = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Günlük Ortalama (Saat)",
    )
    last_calculated = models.DateTimeField(
        auto_now=True,
        verbose_name="Son Hesaplama",
    )

    class Meta:
        verbose_name = "PDKS Aylık Rapor"
        verbose_name_plural = "PDKS Aylık Raporlar"
        unique_together = ("user", "year", "month")
        ordering = ["-year", "-month"]
        indexes = [
            models.Index(fields=["user", "year", "month"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.year}/{self.month:02d} - {self.total_hours} saat"

    def calculate(self):
        """Aylık verileri hesapla"""
        from django.db.models import Sum, Count

        pdks_entries = TeknoparkPDKSEntry.objects.filter(
            user=self.user,
            date__year=self.year,
            date__month=self.month,
        )

        total = pdks_entries.aggregate(
            total=Sum("total_hours"),
            days=Count("id"),
        )

        self.total_hours = total["total"] or 0.00
        self.total_days = total["days"] or 0
        self.average_hours_per_day = (
            round(self.total_hours / self.total_days, 2)
            if self.total_days > 0
            else 0.00
        )
        self.save()
