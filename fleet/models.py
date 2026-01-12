from datetime import timedelta
from django.db import models
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="vehicles",
        null=True,
        blank=True,
    )

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=50, blank=True)
    odometer_reading = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


    def predicted_next_service_km(self):
        services = (
            self.service_history
            .exclude(odometer_at_service__isnull=True)
            .order_by("service_date")
        )

        if services.count() < 2:
            return None

        last = services.last()
        prev = services[services.count() - 2]

        delta = last.odometer_at_service - prev.odometer_at_service
        return last.odometer_at_service + delta if delta > 0 else None

# SERVICE TYPE (CATALOG)

class ServiceType(models.Model):
    name = models.CharField(max_length=120, unique=True)
    default_cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name



# SERVICE HISTORY

class ServiceHistory(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="service_history"
    )

    service_date = models.DateField(default=timezone.now)
    next_service_date = models.DateField(null=True, blank=True)

    reminder_sent = models.BooleanField(default=False)  # ✅ ДОДАТИ

    # legacy
    service_type_text = models.CharField(
        max_length=120,
        null=True,
        blank=True
    )

    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    default_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    notes = models.TextField(blank=True, null=True)
    odometer_at_service = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_overdue(self):
        return (
            self.next_service_date
            and self.next_service_date < timezone.localdate()
        )


# EMAIL TEMPLATE

class EmailTemplate(models.Model):
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# REPORT


class Report(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    include_service_history = models.BooleanField(default=True)
    include_costs = models.BooleanField(default=True)
    include_odometer_analytics = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report: {self.vehicle} ({self.start_date} → {self.end_date})"

    def generate_report(self):
        services_qs = self.vehicle.service_history.filter(
            service_date__gte=self.start_date,
            service_date__lte=self.end_date
        ).order_by("service_date")

        services = list(services_qs)

        total_cost = (
            sum(s.final_cost for s in services)
            if self.include_costs
            else 0
        )

        service_count = len(services)
        avg_cost = (
            total_cost / service_count
            if service_count and self.include_costs
            else 0
        )

        odos = [s.odometer_at_service for s in services if s.odometer_at_service]

        if self.include_odometer_analytics and len(odos) >= 2:
            distance_total = odos[-1] - odos[0]
            days = (services[-1].service_date - services[0].service_date).days or 1

            odo_stats = {
                "has_data": True,
                "distance_total": distance_total,
                "avg_km_per_day": round(distance_total / days, 2),
                "avg_km_between_services": round(
                    distance_total / (len(odos) - 1), 2
                ),
                "samples": len(odos),
            }
        else:
            odo_stats = {
                "has_data": False,
                "samples": len(odos),
            }

        return {
            "services": services,
            "total_cost": float(total_cost),
            "service_count": service_count,
            "avg_cost": float(avg_cost),
            "odo_stats": odo_stats,
            "vehicle": self.vehicle,
            "client": self.vehicle.client,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
