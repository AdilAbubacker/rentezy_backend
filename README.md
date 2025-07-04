# 🏠 RentEzy - Next-Generation Property Management Platform

[![Live Demo](https://img.shields.io/badge/Demo-Live-green)](https://rentezy-frontend-g63i-git-main-adilabubackers-projects.vercel.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](your-github-link)
[![Tech Stack](https://img.shields.io/badge/Stack-Microservices-orange)](#tech-stack)
[![Architecture](https://img.shields.io/badge/Architecture-Event--Driven-purple)](#architecture)

> **Find your next home in minutes, for free.** 
> 
> RentEzy is a enterprise-grade property management platform built with modern microservices architecture, designed to revolutionize how tenants find properties and landlords manage their rentals.

## 🚀 What Makes RentEzy Special

### For Users
- **Lightning-fast property search** powered by Elasticsearch
- **Real-time chat** with landlords and property managers
- **Smart scheduling** for property visits with automated confirmations
- **Secure payments** with automated rent collection and late fee management
- **Instant notifications** for bookings, payments, and updates

### For Developers
- **10+ microservices** architecture with independent scaling
- **Event-driven design** using Apache Kafka for reliable communication
- **Concurrency-safe booking** system preventing race conditions
- **Auto-scaling Kubernetes** deployment on AWS EKS
- **High-performance search** with Elasticsearch clustering

## 🏗️ System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Load Balancer │
│   (React)       │◄───┤   (Django)      │◄───┤   (Nginx)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
        │ Auth Service │ │Booking Svc  │ │Property Svc│
        └──────────────┘ └─────────────┘ └────────────┘
                │               │               │
        ┌───────▼──────────────────────────────▼───────┐
        │           Apache Kafka Event Bus             │
        │         (Event-Driven Communication)         │
        └─────────────────┬────────────────────────────┘
                          │
    ┌─────────────────────┼─────────────────────────────┐
    │                     │                             │
┌───▼────┐    ┌──────▼──────┐    ┌──────▼──────┐    ┌──▼─────┐
│Chat Svc│    │Notification │    │Search Engine│    │Rent Mgmt│
│        │    │Service      │    │(Elasticsearch)│   │Service │
└────────┘    └─────────────┘    └─────────────┘    └────────┘
```

### 🎯 Architectural Decisions

**Why Microservices?**
- **Independent scaling**: Each service scales based on demand
- **Technology diversity**: Best tool for each job
- **Team autonomy**: Different teams can own different services
- **Fault isolation**: Service failures don't cascade

**Event-Driven Design Benefits:**
- **Loose coupling**: Services communicate via events, not direct calls
- **Resilience**: Message persistence ensures no data loss
- **Scalability**: Async processing handles traffic spikes
- **Auditability**: Complete event history for debugging

## 🛠️ Tech Stack

### Backend Microservices
- **Framework**: Django REST Framework
- **Message Broker**: Apache Kafka + Zookeeper
- **Search Engine**: Elasticsearch 
- **Cache & Sessions**: Redis
- **Task Queue**: Celery + Celery Beat
- **Real-time**: WebSockets + Django Channels
- **Database**: PostgreSQL (per service)

### Frontend & Infrastructure
- **Frontend**: React.js + Redux Toolkit + Tailwind CSS
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (AWS EKS)
- **Storage**: AWS EFS CSI Driver
- **Payment**: Stripe Integration
- **Monitoring**: Custom health checks

### DevOps & Deployment
- **Cloud Provider**: Amazon Web Services (AWS)
- **Container Registry**: AWS ECR
- **Load Balancing**: AWS ALB + Nginx
- **CI/CD**: GitHub Actions (implied)
- **Infrastructure**: AWS EKS, EC2, EFS, Route 53

## 🎯 Core Features Deep Dive

### 🔐 Enterprise-Grade Authentication
- **JWT-based authentication** with refresh token rotation
- **Role-based access control** (Tenant, Landlord, Admin)
- **API rate limiting** and request throttling
- **Session management** with Redis backing

### 🏘️ Smart Property Management
- **Advanced property search** with location, price, and amenity filters
- **High-performance indexing** using Elasticsearch
- **Image upload and optimization** with AWS S3 integration
- **Property availability** real-time tracking

### 📅 Intelligent Booking System
- **Concurrency-safe reservations** using database-level locking
- **Automated booking expiry** with Celery scheduled tasks
- **Conflict resolution** for double-booking prevention
- **Visit scheduling** with calendar integration

### 💰 Automated Payment Processing
- **Recurring rent payments** with Celery Beat scheduler
- **Late fee calculation** and automatic application
- **Payment failure handling** with retry mechanisms
- **Transaction history** and receipt generation
- **Stripe webhook integration** for payment confirmations

### 💬 Real-Time Communication
- **WebSocket-based chat** for instant messaging
- **Online presence indicators** showing user status
- **Message delivery confirmation** and read receipts
- **File sharing** capabilities in chat

### 🔔 Event-Driven Notifications
- **Kafka-powered event streaming** for reliable delivery
- **Multi-channel notifications** (in-app, email, SMS ready)
- **Smart notification preferences** per user
- **Real-time delivery** via WebSockets

## 🧩 Microservices Breakdown

| Service | Responsibility | Key Technologies |
|---------|---------------|------------------|
| **api_gateway** | Request routing, auth, rate limiting | Django, JWT |
| **auth_service** | User authentication & authorization | Django, PostgreSQL |
| **property_service** | Property CRUD operations | Django, PostgreSQL |
| **booking_service** | Reservation management | Django, PostgreSQL, Celery |
| **search_service** | Property search & filtering | Django, Elasticsearch |
| **elastic_search** | Search indexing & queries | Elasticsearch |
| **chat_service** | Real-time messaging | Django Channels, WebSockets |
| **notification_service** | Event-driven notifications | Django, Kafka Consumer |
| **rent_service** | Payment processing & automation | Django, Stripe, Celery Beat |
| **schedule_visit** | Visit booking & calendar management | Django, PostgreSQL |
| **kafka** | Event streaming & message broker | Apache Kafka |
| **redis** | Caching & session storage | Redis |

## 🏃‍♂️ Performance & Scalability

### Concurrency Handling
- **Database-level locking** prevents booking race conditions
- **Optimistic locking** for high-traffic scenarios
- **Connection pooling** for database efficiency

### Caching Strategy
- **Redis caching** for frequently accessed data
- **Query optimization** with database indexing
- **API response caching** for improved latency

### Event-Driven Architecture
- **Asynchronous processing** with Kafka messaging
- **Fault tolerance** with message persistence
- **Horizontal scaling** of individual services

### Search Performance
- **Elasticsearch clustering** for high availability
- **Real-time indexing** via Kafka consumers
- **Faceted search** with sub-second response times

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Kubernetes cluster (or minikube for local)
- AWS CLI configured (for cloud deployment)
- Node.js 16+ and Python 3.9+

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/AdilAbubacker/rentezy
cd rentezy

# Start infrastructure services
docker-compose up -d kafka zookeeper redis elasticsearch postgresql

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start microservices (in separate terminals)
python manage.py runserver 8001  # auth_service
python manage.py runserver 8002  # property_service
python manage.py runserver 8003  # booking_service
# ... other services

# Start frontend
cd ../frontend
npm install
npm start
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n rentezy

# Access the application
kubectl port-forward svc/api-gateway 8000:8000
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


<div align="center">

**⭐ Star this repository if you found it helpful!**

[![Made with ❤️ by Adil](https://img.shields.io/badge/Made%20with%20❤️%20by-Adil-red)](https://github.com/your-username)

</div>
