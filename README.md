Fleet Management System (Django)
A simple fleet management web application built with Django, designed to manage vehicles, service history, clients, and reports.
The project was created as a learning & portfolio project, with a strong focus on clean architecture, business logic, and real-world use cases.

Features
Vehicles

Vehicle registry (make, model, year, VIN, mileage)
Vehicles assigned to clients
Mileage-based service prediction
> Service Management
Service history per vehicle
Service types catalog with default prices
Custom service cost support
Overdue service detection
Upcoming service tracking
Total service cost calculation
HTMX-based dynamic UI (no full page reloads)
>Clients
Client management (name, contact info, notes)
One client can own multiple vehicles
>Reports
Vehicle service reports
Date range filtering
Cost summary
Odometer analytics
Average cost and usage statistics
>Smart Logic
Predicted next service mileage
Overdue service flag based on dates
Aggregated analytics per vehicle
> Tech Stack
Python 3
Django 5 / 6
PostgreSQL
HTMX
HTML + CSS (no frontend framework)
Docker (development environment)
📂 Project Structure (simplified)
fleet/
├── models.py
├── views/
│   ├── services.py
│   ├── reports.py
│   └── dashboard.py
├── routes/
│   ├── services.py
│   ├── reports.py
│   └── vehicles.py
templates/
├── service/
├── reports/
├── dashboard/

Running the Project
Using Docker
docker compose up --build

Migrations
docker compose exec web python manage.py migrate

Create superuser
docker compose exec web python manage.py createsuperuser

 Project Goals

Practice Django architecture and patterns

Model real business logic (clients → vehicles → services → reports)

Build a realistic CRUD system

Prepare a solid portfolio project for junior/mid backend roles

Possible Future Improvements

PDF export for reports

Email notifications for overdue services

Permissions & authentication

REST API

Charts and dashboards

📌 Notes

This project intentionally prioritizes clarity, logic, and structure over advanced frontend styling or micro-optimizations.
