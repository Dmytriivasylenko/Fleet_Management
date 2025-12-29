# fleet/views/driver.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ..forms import DriverForm
from ..models import Driver

class DriverListView(ListView):
    model = Driver
    template_name = "drivers/driver_list.html"
    context_object_name = "drivers"
    paginate_by = 10

class DriverCreateView(CreateView):
    model = Driver
    form_class = DriverForm
    template_name = "drivers/driver_form.html"
    success_url = reverse_lazy("driver_list")

    def form_valid(self, form):
        driver = form.save()
        if self.request.htmx:
            return render(self.request, "drivers/partials/driver_row.html", {"driver": driver})
        return redirect(self.success_url)

class DriverUpdateView(UpdateView):
    model = Driver
    form_class = DriverForm
    template_name = "drivers/driver_form.html"
    success_url = reverse_lazy("driver_list")

    def form_valid(self, form):
        driver = form.save()
        if self.request.htmx:
            return render(self.request, "drivers/partials/driver_row.html", {"driver": driver})
        return redirect(self.success_url)

class DriverDeleteView(DeleteView):
    model = Driver
    template_name = "drivers/driver_confirm_delete.html"
    success_url = reverse_lazy("driver_list")

    def delete(self, request, *args, **kwargs):
        driver = self.get_object()
        driver.delete()
        if request.htmx:
            return HttpResponse(status=204)
        return redirect(self.success_url)
