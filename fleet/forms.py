# fleet/forms.py
from django import forms

from .models import (
    Vehicle,
    Client,
    ServiceHistory,
    EmailTemplate,
    Report,
)

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone", "notes"]


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "make",
            "model",
            "year",
            "vin",
            "odometer_reading",
        ]
class ServiceHistoryForm(forms.ModelForm):
    class Meta:
        model = ServiceHistory
        fields = (
            "service_type",
            "service_date",
            "final_cost",
            "notes",
            "next_service_date",
            "odometer_at_service",
        )

# ==========================
# EMAIL TEMPLATE
# ==========================
class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = [
            "name",
            "subject",
            "body",
        ]


# ==========================
# REPORT
# ==========================
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            "vehicle",
            "start_date",
            "end_date",
            "include_service_history",
            "include_costs",
            "include_odometer_analytics",
        ]

# fleet/forms.py

