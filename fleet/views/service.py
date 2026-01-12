from datetime import date
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum, Avg
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import TemplateView
from ..forms import ServiceHistoryForm
from ..models import Vehicle, ServiceHistory, ServiceType


# ENTRY PAGE


class ServiceHistoryPageView(TemplateView):
    template_name = "service/service_history_page.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["vehicles"] = Vehicle.objects.all()
        ctx["vehicle"] = None
        return ctx



# VEHICLE WORKSPACE (HTMX)


class ServiceHistoryVehicleView(TemplateView):
    template_name = "service/vehicle_workspace.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        vehicle = get_object_or_404(Vehicle, pk=self.kwargs["vehicle_id"])
        today = timezone.localdate()

        services = (
            ServiceHistory.objects
            .filter(vehicle=vehicle)
            .select_related("service_type")
            .order_by("-service_date")
        )

        overdue = services.filter(
            next_service_date__lt=today
        )

        upcoming = services.filter(
            next_service_date__gte=today
        ).order_by("next_service_date")[:5]

        ctx.update({
            "vehicle": vehicle,
            "service_types": ServiceType.objects.filter(is_active=True),
            "service_histories": services,
            "today": today,
            "total_cost": services.aggregate(
                total=Sum("final_cost")
            )["total"] or 0,
            "overdue_services": overdue,
            "upcoming_services": upcoming,
            "predicted_km": vehicle.predicted_next_service_km()
            if hasattr(vehicle, "predicted_next_service_km")
            else None,
        })

        return ctx


# ADD SERVICE


@require_POST
def add_service_htmx(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    form = ServiceHistoryForm(request.POST)

    if not form.is_valid():
        return HttpResponse(status=400)

    service = form.save(commit=False)
    service.vehicle = vehicle

    if service.service_type:
        service.default_cost = service.service_type.default_cost
        service.final_cost = service.final_cost or service.default_cost

    service.save()

    return render(request, "service/partials/service_row.html", {
        "service": service,
        "today": timezone.localdate(),
    })



# DELETE


@require_http_methods(["DELETE"])
def service_delete(request, vehicle_id, pk):
    service = get_object_or_404(ServiceHistory, pk=pk, vehicle_id=vehicle_id)
    service.delete()
    return render(request, "service/partials/empty_row.html")



# INLINE COST EDIT


def service_cost_edit(request, vehicle_id, pk):
    service = get_object_or_404(ServiceHistory, pk=pk, vehicle_id=vehicle_id)
    return render(request, "service/partials/service_cost_edit.html", {
        "service": service
    })


@require_POST
def service_cost_update(request, vehicle_id, pk):
    service = get_object_or_404(ServiceHistory, pk=pk, vehicle_id=vehicle_id)
    service.final_cost = request.POST.get("final_cost") or service.final_cost
    service.save()

    return render(request, "service/partials/service_row.html", {
        "service": service,
        "today": timezone.localdate(),
    })
