from django.urls import path

from . import views
from .views import (

    # Drivers
    DriverListView, DriverCreateView, DriverUpdateView, DriverDeleteView,

    # Vehicles
    VehicleListView, VehicleCreateView, VehicleUpdateView, VehicleDeleteView,
    vehicle_form_modal, add_vehicle_htmx, vehicle_delete_htmx,

    # Services
    ServiceHistoryListView,
    add_service_htmx,
    service_field_edit, service_field_save,
    service_duplicate,
    service_delete,
    service_row_reload,
    service_history_search, service_history_filter,
    service_history_sort, service_history_date_filter, service_history_cost_filter,

    # Email template
)
from .views.email_templates import EmailTemplateListView, EmailTemplateCreateView, EmailTemplateUpdateView
from .views.home import home
from .views.reports import ReportListView, ReportCreateView, report_detail

urlpatterns = [

    # HOME
    path("", home, name="home"),

    # DRIVERS
    path("drivers/", DriverListView.as_view(), name="driver_list"),
    path("drivers/add/", DriverCreateView.as_view(), name="driver_create"),
    path("drivers/<int:pk>/edit/", DriverUpdateView.as_view(), name="driver_update"),
    path("drivers/<int:pk>/delete/", DriverDeleteView.as_view(), name="driver_delete"),

    # VEHICLES
    path("vehicles/", VehicleListView.as_view(), name="vehicle_list"),
    path("vehicles/create/", VehicleCreateView.as_view(), name="vehicle_create"),
    path("vehicles/<int:pk>/update/", VehicleUpdateView.as_view(), name="vehicle_update"),
    path("vehicles/<int:pk>/delete/", VehicleDeleteView.as_view(), name="vehicle_delete"),

    # VEHICLE HTMX
    path("vehicle/modal/", vehicle_form_modal, name="vehicle_form_modal"),
    path("vehicle/add-htmx/", add_vehicle_htmx, name="add_vehicle_htmx"),
    path("vehicle/<int:pk>/delete-htmx/", vehicle_delete_htmx, name="vehicle_delete_htmx"),

    # SERVICE LIST
    path("service-history/", ServiceHistoryListView.as_view(), name="service_history_list"),

    # SERVICE CRUD
    path("service/add-htmx/", add_service_htmx, name="add_service_htmx"),
    #path("service/<int:pk>/detail-htmx/", service_detail_htmx, name="service_detail_htmx"),
    path("service/<int:pk>/edit/<str:field>/", service_field_edit, name="service_field_edit"),
    path("service/<int:pk>/save/<str:field>/", service_field_save, name="service_field_save"),
    path("service/<int:pk>/duplicate/", service_duplicate, name="service_duplicate"),
    path("service/<int:pk>/delete/", service_delete, name="service_delete"),
    path("service/<int:pk>/row/", service_row_reload, name="service_row_reload"),

    # FILTERS
    path("service-history/search/", service_history_search, name="service_history_search"),
    path("service-history/filter/", service_history_filter, name="service_history_filter"),
    path("service-history/sort/", service_history_sort, name="service_history_sort"),
    path("service-history/date-filter/", service_history_date_filter, name="service_history_date_filter"),
    path("service-history/cost-filter/", service_history_cost_filter, name="service_history_cost_filter"),

    # REPORTS
    path("reports/", ReportListView.as_view(), name="report_list"),
    path("reports/create/", ReportCreateView.as_view(), name="create_report"),
    path("reports/<int:report_id>/", report_detail, name="report_detail"),

    # EMAIL TEMPLATES
    path("email-templates/", EmailTemplateListView.as_view(), name="emailtemplate_list"),
    path("email-templates/create/", EmailTemplateCreateView.as_view(), name="emailtemplate_create"),
    path("email-templates/<int:pk>/edit/", EmailTemplateUpdateView.as_view(), name="emailtemplate_edit"),

# HTMX detail / edit / update
    path('service/<int:pk>/detail-htmx/', views.service_detail_htmx, name='service_detail_htmx'),
    path('service/<int:pk>/edit-htmx/', views.service_edit_htmx, name='service_edit_htmx'),
    path('service/<int:pk>/update-htmx/', views.service_update_htmx, name='service_update_htmx'),



]


