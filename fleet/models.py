from datetime import timedelta
from django.db import models
from django.utils import timezone


# ==========================
# VEHICLE
# ==========================
class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=50, blank=True)
    odometer_reading = models.IntegerField(default=0)  # останній відомий пробіг

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


# ==========================
# DRIVER
# ==========================
class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    assigned_car = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# ==========================
# SERVICE HISTORY
# ==========================
class ServiceHistory(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="service_history")
    service_date = models.DateField(default=timezone.now)
    service_type = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    next_service_date = models.DateField(null=True, blank=True)

    # Нове поле — пробіг автомобіля на момент сервісу
    odometer_at_service = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Якщо механік не вказав дату наступного сервісу → ставимо +180 днів
        if not self.next_service_date:
            self.next_service_date = self.service_date + timedelta(days=180)

        # Якщо вказано пробіг — оновлюємо пробіг авто
        if self.odometer_at_service and self.vehicle.odometer_reading < self.odometer_at_service:
            self.vehicle.odometer_reading = self.odometer_at_service
            self.vehicle.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service_date} — {self.service_type} ({self.vehicle})"


# ==========================
# EMAIL TEMPLATE
# ==========================
class EmailTemplate(models.Model):
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ==========================
# REPORT (єдина правильна версія)
# ==========================
class Report(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    include_service_history = models.BooleanField(default=True)
    include_costs = models.BooleanField(default=True)
    include_odometer_analytics = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report: {self.vehicle} ({self.start_date} → {self.end_date})"

    # ==========================
    # Генератор звіту
    # ==========================
    def generate_report(self):
        services_qs = self.vehicle.service_history.filter(
            service_date__gte=self.start_date,
            service_date__lte=self.end_date
        ).order_by("service_date")

        service_list = list(services_qs)
        total_cost = sum([s.cost for s in service_list]) if self.include_costs else 0
        service_count = len(service_list)
        avg_cost = (total_cost / service_count) if service_count and self.include_costs else 0

        # Пробіг — аналіз
        odos = [s.odometer_at_service for s in service_list if s.odometer_at_service]

        if self.include_odometer_analytics and len(odos) >= 2:
            distance_total = odos[-1] - odos[0]
            days = (service_list[-1].service_date - service_list[0].service_date).days or 1

            odo_stats = {
                "has_data": True,
                "distance_total": distance_total,
                "avg_km_per_day": round(distance_total / days, 2),
                "avg_km_between_services": round(distance_total / (len(odos) - 1), 2),
                "samples": len(odos),
            }
        else:
            odo_stats = {
                "has_data": False,
                "samples": len(odos),
            }

        return {
            "services": service_list,
            "total_cost": float(total_cost),
            "service_count": service_count,
            "avg_cost": float(avg_cost),
            "odo_stats": odo_stats,
            "vehicle": self.vehicle,
            "driver": self.driver,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
