Fleet Management System (Django)

A clean, production-style fleet management system built with Django to manage clients, vehicles, service history, reminders, and reports.

This project was designed as a portfolio-ready educational project, focusing on:

clear domain logic

maintainable architecture

realistic business features

clean UI (no heavy frontend frameworks)

✨ Features Overview
👤 Clients

Full CRUD for clients

Each client can own multiple vehicles

Client-centric data model (vehicles & services belong to clients)

Designed for B2B / service-based workflows

🚘 Vehicles

Vehicles assigned to clients

Track make, model, year, VIN, odometer

Vehicle-level analytics

Predictive next service mileage

🛠️ Service Management

Service history per vehicle

Service types with default pricing

Custom service costs supported

Odometer tracking per service

Next service date support

Overdue service detection

Smart UI badges (overdue / custom cost)

🔔 Service Reminders (logic-ready)

Overdue services detected automatically

Reminder flags prepared for email notifications

Email templates stored in database

Ready for async processing via Celery

Email sending intentionally left as placeholder to keep project lightweight and portable.

📊 Dashboard

Global overview of fleet health

KPI cards:

total vehicles

overdue services

recent services

Upcoming & overdue services panels

Designed for future chart integration

📄 Reports

Vehicle-based reports

Date range filtering

KPIs:

total cost

service count

average cost

Odometer analytics:

distance driven

average km/day

average km between services

CSV export (PDF intentionally avoided for portability)

Client-aware report context

📤 Export

CSV export for reports

Simple, reliable, dependency-free

Easy to import into Excel / Google Sheets

🧠 Architecture & Design Decisions
Why no PDF?

PDF generation often introduces heavy OS-level dependencies.
CSV was chosen for:

simplicity

portability

real-world usefulness

Why HTMX?

Minimal JavaScript

Server-driven UI

Clean HTML templates

No SPA complexity

Why Client-centric model?

Real-world fleet/service systems are client-driven:

Client → Vehicles → Services → Reports


This structure scales naturally for:

service companies

leasing fleets

internal corporate fleets

🗂️ Project Structure
fleet/
├── models.py          # Domain models
├── views/
│   ├── dashboard.py
│   ├── services.py
│   ├── reports.py
│   └── clients.py
├── routes/
│   ├── dashboard.py
│   ├── services.py
│   ├── reports.py
│   └── clients.py
├── templates/
│   ├── base.html
│   ├── dashboard/
│   ├── service/
│   ├── reports/
│   └── clients/