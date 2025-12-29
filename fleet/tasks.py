from celery import shared_task
from django.core.mail import send_mail
from .models import ServiceHistory



@shared_task
def send_service_notification(service_id):
    service = ServiceHistory.objects.get(id=service_id)
    subject = f"Reminder: Service needed for {service.vehicle}"
    message = f"Vehicle {service.vehicle} is due for service on {service.next_service_date}."
    recipient_list = ['vasylenko185@gmail.com']
    send_mail(subject, message, 'vasylenkodmytrii@gmail.com', recipient_list)