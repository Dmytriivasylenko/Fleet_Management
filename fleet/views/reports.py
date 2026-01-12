from django.utils import timezone
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from fleet.models import Vehicle, ServiceHistory


class ReportSelectView(TemplateView):
    template_name = "reports/report_select.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["vehicles"] = Vehicle.objects.all()
        ctx["today"] = timezone.localdate()
        return ctx


class VehicleReportView(TemplateView):
    template_name = "reports/vehicle_report.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        vehicle = get_object_or_404(Vehicle, pk=self.kwargs["vehicle_id"])
        date_from = self.request.GET.get("from")
        date_to = self.request.GET.get("to")

        services = ServiceHistory.objects.filter(vehicle=vehicle)

        if date_from:
            services = services.filter(service_date__gte=date_from)
        if date_to:
            services = services.filter(service_date__lte=date_to)

        services = services.select_related("service_type").order_by("service_date")

        total_cost = sum(s.final_cost for s in services)
        service_count = services.count()
        avg_cost = round(total_cost / service_count, 2) if service_count else 0

        overdue = services.filter(
            next_service_date__lt=timezone.localdate()
        )

        predicted_km = vehicle.predicted_next_service_km()

        ctx.update({
            "vehicle": vehicle,
            "services": services,
            "date_from": date_from,
            "date_to": date_to,
            "total_cost": total_cost,
            "service_count": service_count,
            "avg_cost": avg_cost,
            "overdue_services": overdue,
            "predicted_km": predicted_km,
        })

        return ctx
