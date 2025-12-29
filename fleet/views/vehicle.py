# fleet/views/vehicle.py
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..forms import VehicleForm
from ..models import Vehicle

class VehicleListView(ListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"
    context_object_name = "vehicles"
    paginate_by = 10

class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicle_list")

class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicle_list")

class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = "vehicles/vehicle_confirm_delete.html"
    success_url = reverse_lazy("vehicle_list")

def vehicle_form_modal(request):
    return render(request, "partials/vehicle_form_modal.html", {"vehicle_form": VehicleForm()})

@require_POST
def add_vehicle_htmx(request):
    form = VehicleForm(request.POST)
    if form.is_valid():
        vehicle = form.save()
        # return option snippet (to append + set selected client-side)
        return render(request, "partials/vehicle_option.html", {"vehicle": vehicle})
    return HttpResponseBadRequest(form.errors.as_json())

@require_http_methods(["DELETE"])
def vehicle_delete_htmx(pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return HttpResponse(status=204)
