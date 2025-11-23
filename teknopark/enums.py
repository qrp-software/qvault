from django.db.models import TextChoices, IntegerChoices


class PDKSLogType(TextChoices):
    ENTRY = "entry", "Giriş"
    EXIT = "exit", "Çıkış"


class MonthChoices(IntegerChoices):
    """Ay seçenekleri"""

    JANUARY = 1, "Ocak"
    FEBRUARY = 2, "Şubat"
    MARCH = 3, "Mart"
    APRIL = 4, "Nisan"
    MAY = 5, "Mayıs"
    JUNE = 6, "Haziran"
    JULY = 7, "Temmuz"
    AUGUST = 8, "Ağustos"
    SEPTEMBER = 9, "Eylül"
    OCTOBER = 10, "Ekim"
    NOVEMBER = 11, "Kasım"
    DECEMBER = 12, "Aralık"
