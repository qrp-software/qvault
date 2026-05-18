from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from teknopark.models import (
	TeknoparkPDKSEntry,
	TeknoparkPDKSEntryLog,
	TeknoparkPDKSMonthlyReport,
	TeknoparkUser,
)


class SuperUserRequiredMixin(UserPassesTestMixin):
	"""Sadece superuser kullanicilarin erisebilecegi view'lar."""

	def test_func(self):
		return self.request.user.is_superuser


class TeknoparkUserListView(LoginRequiredMixin, SuperUserRequiredMixin, View):
	template_name = "teknopark/admin_user_list.html"

	def get(self, request):
		search_query = request.GET.get("search", "").strip()
		users = TeknoparkUser.objects.select_related("user").order_by("-created_date")

		if search_query:
			users = users.filter(
				Q(user__username__icontains=search_query)
				| Q(user__first_name__icontains=search_query)
				| Q(user__last_name__icontains=search_query)
				| Q(user__email__icontains=search_query)
			)

		context = {
			"teknopark_users": users,
			"search_query": search_query,
			"active_count": users.filter(is_active=True).count(),
		}
		return render(request, self.template_name, context)


class TeknoparkUserDetailView(LoginRequiredMixin, SuperUserRequiredMixin, View):
	template_name = "teknopark/admin_user_detail.html"

	def get(self, request, teknopark_user_id):
		teknopark_user = get_object_or_404(
			TeknoparkUser.objects.select_related("user"),
			id=teknopark_user_id,
		)

		entries = TeknoparkPDKSEntry.objects.filter(teknopark_user=teknopark_user)
		monthly_reports = TeknoparkPDKSMonthlyReport.objects.filter(
			teknopark_user=teknopark_user
		)

		total_hours = entries.aggregate(total=Sum("total_hours"))["total"]

		context = {
			"teknopark_user": teknopark_user,
			"total_log_count": TeknoparkPDKSEntryLog.objects.filter(
				teknopark_user=teknopark_user
			).count(),
			"total_entry_days": entries.count(),
			"last_entry": entries.order_by("-date").first(),
			"last_report": monthly_reports.order_by("-year", "-month").first(),
			"total_hours": total_hours or 0,
		}
		return render(request, self.template_name, context)


class TeknoparkPDKSEntryLogListView(LoginRequiredMixin, SuperUserRequiredMixin, View):
	template_name = "teknopark/admin_entry_log_list.html"

	def get(self, request, teknopark_user_id):
		teknopark_user = get_object_or_404(
			TeknoparkUser.objects.select_related("user"),
			id=teknopark_user_id,
		)
		log_type = request.GET.get("log_type", "").strip()

		logs = TeknoparkPDKSEntryLog.objects.filter(teknopark_user=teknopark_user).order_by(
			"-timestamp"
		)

		if log_type:
			logs = logs.filter(log_type=log_type)

		context = {
			"teknopark_user": teknopark_user,
			"logs": logs,
			"selected_log_type": log_type,
		}
		return render(request, self.template_name, context)


class TeknoparkPDKSEntryListView(LoginRequiredMixin, SuperUserRequiredMixin, View):
	template_name = "teknopark/admin_entry_list.html"

	def get(self, request):
		search_query = request.GET.get("search", "").strip()

		entries = TeknoparkPDKSEntry.objects.select_related(
			"teknopark_user", "teknopark_user__user"
		).order_by("-date")

		if search_query:
			entries = entries.filter(
				Q(teknopark_user__user__username__icontains=search_query)
				| Q(teknopark_user__user__first_name__icontains=search_query)
				| Q(teknopark_user__user__last_name__icontains=search_query)
			)

		context = {
			"entries": entries,
			"search_query": search_query,
			"total_hours": entries.aggregate(total=Sum("total_hours"))["total"] or 0,
		}
		return render(request, self.template_name, context)


class TeknoparkPDKSMonthlyReportListView(LoginRequiredMixin, SuperUserRequiredMixin, View):
	template_name = "teknopark/admin_monthly_report_list.html"

	def post(self, request):
		teknopark_user_id = request.POST.get("teknopark_user_id", "").strip()
		year_value = request.POST.get("year", "").strip()
		month_value = request.POST.get("month", "").strip()

		if not (teknopark_user_id.isdigit() and year_value.isdigit() and month_value.isdigit()):
			messages.error(request, "Lutfen gecerli kullanici, yil ve ay secin.")
			return redirect("teknopark:admin_monthly_report_list")

		month = int(month_value)
		if month < 1 or month > 12:
			messages.error(request, "Ay 1 ile 12 arasinda olmalidir.")
			return redirect("teknopark:admin_monthly_report_list")

		teknopark_user = TeknoparkUser.objects.filter(id=int(teknopark_user_id)).first()
		if not teknopark_user:
			messages.error(request, "Secilen teknopark kullanicisi bulunamadi.")
			return redirect("teknopark:admin_monthly_report_list")

		report, created = TeknoparkPDKSMonthlyReport.objects.get_or_create(
			teknopark_user=teknopark_user,
			year=int(year_value),
			month=month,
		)
		report.calculate()

		if created:
			messages.success(request, "Aylik rapor basariyla olusturuldu ve hesaplandi.")
		else:
			messages.success(request, "Aylik rapor yeniden hesaplandi.")

		return redirect("teknopark:admin_monthly_report_list")

	def get(self, request):
		search_query = request.GET.get("search", "").strip()
		year = request.GET.get("year", "").strip()
		month = request.GET.get("month", "").strip()

		reports = TeknoparkPDKSMonthlyReport.objects.select_related(
			"teknopark_user", "teknopark_user__user"
		).order_by("-year", "-month")

		if search_query:
			reports = reports.filter(
				Q(teknopark_user__user__username__icontains=search_query)
				| Q(teknopark_user__user__first_name__icontains=search_query)
				| Q(teknopark_user__user__last_name__icontains=search_query)
			)

		if year.isdigit():
			reports = reports.filter(year=int(year))

		if month.isdigit():
			reports = reports.filter(month=int(month))

		context = {
			"reports": reports,
			"search_query": search_query,
			"selected_year": year,
			"selected_month": month,
			"teknopark_users": TeknoparkUser.objects.select_related("user").order_by("user__username"),
			"default_year": timezone.now().year,
			"default_month": timezone.now().month,
			"years": (
				TeknoparkPDKSMonthlyReport.objects.values_list("year", flat=True)
				.distinct()
				.order_by("-year")
			),
			"months": range(1, 13),
		}
		return render(request, self.template_name, context)
