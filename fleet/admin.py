from django.contrib import admin
from .models import ServiceType

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "default_cost", "is_active", "sort_order")
    list_editable = ("default_cost", "is_active", "sort_order")
    ordering = ("sort_order", "name")