# fleet/views/service.py
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import ListView

from ..forms import ServiceHistoryForm, VehicleForm
from ..models import Vehicle, ServiceHistory

# Service history list view (CBV)
class ServiceHistoryListView(ListView):
    model = ServiceHistory
    template_name = "service/service_history_list.html"
    context_object_name = "service_histories"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["vehicles"] = Vehicle.objects.all()
        ctx["service_form"] = ServiceHistoryForm()
        ctx["vehicle_form"] = VehicleForm()
        ctx["today"] = timezone.localdate()
        return ctx

# HTMX: add service
@require_POST
def add_service_htmx(request):
    form = ServiceHistoryForm(request.POST)
    if form.is_valid():
        service = form.save()
        # Return the new table row partial. Frontend can reset the form on htmx:afterOnLoad
        return render(request, "service/partials/service_row.html", {
            "service": service,
            "today": timezone.localdate()
        })
    return HttpResponseBadRequest(form.errors.as_json())

# Panel detail
def service_detail_htmx(request, pk):
    service = get_object_or_404(ServiceHistory, pk=pk)
    return render(request, "service/partials/service_detail_panel.html", {
        "service": service,
        "today": timezone.localdate()
    })

# Duplicate service
@require_POST
def service_duplicate(request, pk):
    src = get_object_or_404(ServiceHistory, pk=pk)
    src.pk = None
    new = src
    new.save()
    return render(request, "service/partials/service_row.html", {
        "service": new,
        "today": timezone.localdate()
    })

# Reload one row (useful after edits)
def service_row_reload(request, pk):
    service = get_object_or_404(ServiceHistory, pk=pk)
    return render(request, "service/partials/service_row.html", {
        "service": service,
        "today": timezone.localdate()
    })

# Delete service
@require_http_methods(["DELETE"])
def service_delete(request, pk):
    service = get_object_or_404(ServiceHistory, pk=pk)
    service.delete()
    return HttpResponse(status=204)

# Inline edit GET (returns editable input)
@require_http_methods(["GET"])
def service_field_edit(request, pk, field):
    service = get_object_or_404(ServiceHistory, pk=pk)
    return render(request, "service/partials/service_field_edit.html", {
        "service": service,
        "field": field,
        "value": getattr(service, field)
    })

# Inline edit save
@require_http_methods(["POST"])
def service_field_save(request, pk, field):
    service = get_object_or_404(ServiceHistory, pk=pk)
    value = request.POST.get("value")

    # Basic validation
    if field == "cost":
        try:
            value = float(value)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid cost")

    # For date fields we rely on model to coerce string -> date, or you can parse explicitly
    setattr(service, field, value)
    service.save()

    # If client requested panel refresh, return panel partial
    if request.POST.get("return_panel") or request.GET.get("return_panel"):
        return render(request, "service/partials/service_detail_panel.html", {
            "service": service,
            "today": timezone.localdate()
        })

    return render(request, "service/partials/service_row.html", {
        "service": service,
        "today": timezone.localdate()
    })

# Filters / search / sort endpoints (return table body partial)
def service_history_filter(request):
    vehicle_id = request.GET.get("vehicle")
    if vehicle_id:
        services = ServiceHistory.objects.filter(vehicle_id=vehicle_id)
    else:
        services = ServiceHistory.objects.all()
    services = services.order_by("-service_date")
    return render(request, "service/partials/services_table_body.html", {
        "service_histories": services,
        "today": timezone.localdate()
    })

def service_history_search(request):
    query = request.GET.get("search", "").strip()
    if query:
        services = ServiceHistory.objects.filter(
            Q(service_type__icontains=query) |
            Q(notes__icontains=query) |
            Q(cost__icontains=query) |
            Q(vehicle__make__icontains=query) |
            Q(vehicle__model__icontains=query) |
            Q(vehicle__year__icontains=query)
        )
    else:
        services = ServiceHistory.objects.all()
    services = services.order_by("-service_date")
    return render(request, "service/partials/services_table_body.html", {
        "service_histories": services,
        "today": timezone.localdate()
    })

def service_history_sort(request):
    column = request.GET.get("column")
    direction = request.GET.get("direction")
    allowed = {
        "vehicle": "vehicle__make",
        "service_type": "service_type",
        "cost": "cost",
        "next_service_date": "next_service_date",
        "service_date": "service_date",
    }
    sort_column = allowed.get(column, "service_date")
    if direction == "desc":
        sort_column = "-" + sort_column
    services = ServiceHistory.objects.all().order_by(sort_column)
    return render(request, "service/partials/services_table_body.html", {
        "service_histories": services,
        "today": timezone.localdate()
    })

def service_history_date_filter(request):
    date_from = request.GET.get("from")
    date_to = request.GET.get("to")
    services = ServiceHistory.objects.all()
    if date_from:
        services = services.filter(service_date__gte=date_from)
    if date_to:
        services = services.filter(service_date__lte=date_to)
    services = services.order_by("-service_date")
    return render(request, "service/partials/services_table_body.html", {
        "service_histories": services,
        "today": timezone.localdate()
    })

def service_history_cost_filter(request):
    cost_min = request.GET.get("min")
    cost_max = request.GET.get("max")
    services = ServiceHistory.objects.all()
    if cost_min:
        services = services.filter(cost__gte=cost_min)
    if cost_max:
        services = services.filter(cost__lte=cost_max)
    services = services.order_by("-service_date")
    return render(request, "service/partials/services_table_body.html", {
        "service_histories": services,
        "today": timezone.localdate()
    })

# Extra: edit full service form in panel (GET/POST)
@require_http_methods(["GET"])
def service_edit_htmx(request, pk):
    service = get_object_or_404(ServiceHistory, pk=pk)
    form = ServiceHistoryForm(instance=service)
    return render(request, "service/partials/service_edit_form.html", {"form": form, "service": service})

@require_http_methods(["POST"])
def service_update_htmx(request, pk):
    service = get_object_or_404(ServiceHistory, pk=pk)
    form = ServiceHistoryForm(request.POST, instance=service)
    if form.is_valid():
        service = form.save()
        return render(request, "service/partials/service_detail_panel.html", {"service": service, "today": timezone.localdate()})
    return render(request, "service/partials/service_edit_form.html", {"form": form, "service": service})
