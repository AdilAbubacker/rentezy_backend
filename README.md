# 🏡 RentEzy – Scalable Property Management & Rental Platform

> A modern, full-stack, microservice-based property management system enabling listings, bookings, rent automation, and real-time communication.

---

## 🚀 Features

- 🔍 Property Listings with advanced search & filters
- 📅 Booking System with transactional safety
- 💬 Real-time Chat & Notifications via WebSockets
- 💸 Automated Rent Payments (monthly cycles with late fees)
- 🔐 JWT-based Auth System + Role Management
- 🔄 Microservice Architecture with Kafka
- 📊 Scalable Search with Elasticsearch
- 💳 Stripe Integration for secure transactions
- 🧾 Admin Dashboard for rent & tenant management

---

## 🛠️ Tech Stack

| Layer         | Tools & Tech                                                |
|---------------|-------------------------------------------------------------|
| Frontend      | React.js, Redux Toolkit, Tailwind CSS                       |
| Backend       | Django REST Framework, Django Channels                      |
| Messaging     | Apache Kafka (inter-service communication)                  |
| Tasks         | Celery, Celery Beat (automated rent, reminders)             |
| Realtime      | WebSockets (via Django Channels)                            |
| Search        | Elasticsearch                                               |
| Payments      | Stripe (Recurring + One-Time)                               |
| Auth & API    | JWT Auth, Django API Gateway                                |
| DevOps        | Docker, Kubernetes (EKS), AWS EC2, EFS, Nginx, Gunicorn     |
| DBs           | PostgreSQL, Redis                                           |

---

## 🧩 System Architecture

![Architecture Diagram](https://via.placeholder.com/800x400.png?text=RentEzy+System+Architecture)

> .

---

## 🔄 Microservices Overview

| Service             | Description                                               |
|---------------------|-----------------------------------------------------------|
| Auth Service        | User login, JWT auth, permission management               |
| Property Service    | Listings, filters, CRUD, Elasticsearch sync               |
| Booking Service     | Safe booking with DB-level locks, payment validation      |
| Chat & Notification | Real-time socket updates + reminders via Celery           |
| Payment Service     | Stripe integration, refunds, retries                      |
| Scheduler Service   | Recurring rent collection, auto-fee appending             |

---

## 📦 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/AdilAbubacker/rentezy_backend.git
cd rentezy_backend
