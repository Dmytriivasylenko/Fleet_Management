from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from ..models import Report
from ..forms import ReportForm

class ReportListView(ListView):
    model = Report
    template_name = "reports/report_list.html"
    context_object_name = "reports"
    paginate_by = 20


class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = "reports/create_report.html"
    success_url = reverse_lazy("report_list")

    def form_valid(self, form):
        report = form.save()
        return redirect("report_detail", report_id=report.id)


def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    data = report.generate_report()
    return render(request, "reports/report_detail.html", {"report": report, "data": data})
