# fleet/forms.py
from django import forms
from .models import Driver, Vehicle, ServiceHistory, EmailTemplate, Report

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'phone_number', 'assigned_car']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'vin', 'odometer_reading']


class ServiceHistoryForm(forms.ModelForm):
    class Meta:
        model = ServiceHistory
        fields = ['vehicle', 'service_date', 'service_type', 'cost', 'odometer_at_service', 'next_service_date', 'notes']


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['vehicle', 'driver', 'start_date', 'end_date', 'include_service_history', 'include_costs', 'include_odometer_analytics']
