from django.urls import path, include
from .views.home import home
from .views.services_reminders import service_reminders_preview

app_name = "fleet"

urlpatterns = [
    path("", include(("fleet.routes.dashboard", "dashboard"), namespace="dashboard")),
    path("clients/", include(("fleet.routes.clients", "clients"), namespace="clients")),

    path("vehicles/", include("fleet.routes.vehicles")),
    path("service-history/", include(("fleet.routes.services", "services"), namespace="services")),
    path(
        "reports/",
        include(("fleet.routes.reports", "reports"), namespace="reports"),
    ),
    path("reminders/preview/", service_reminders_preview, name="service_reminders_preview"),

    path("service-types/", include("fleet.routes.service_types")),
]
