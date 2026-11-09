# AI Smart Citizen Grievance System

An intelligent, AI-powered citizen grievance classification and department workflow management system built with **FastAPI**, **PostgreSQL**, **Scikit-Learn ML**, and modern web frontends, fully containerized with **Docker** and **Docker Compose**.

---

## Architecture Overview

```
                          ┌───────────────────────────────┐
                          │   Citizen Portal & Officer    │
                          │   Frontend (Nginx / Web)      │
                          │        Port 5500              │
                          └──────────────┬────────────────┘
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │         FastAPI Backend API           │
                     │       Ports 8000 / 8001 / 8002        │
                     │  - Citizen Complaints API (/complaints)│
                     │  - Officer Auth API (/officer/login)  │
                     │  - Officer Dashboard API              │
                     │  - ML Classification & Rule Engine    │
                     └───────────────────┬───────────────────┘
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │          PostgreSQL Database          │
                     │               Port 5432               │
                     │  - citizens, complaints, officers     │
                     └───────────────────────────────────────┘
```

---

## Quick Start with Docker

### 1. Start All Services
```bash
docker compose up -d --build
```

### 2. Verify Container Health
```bash
docker compose ps
```

All three services (`grievance_db`, `grievance_api`, `grievance_frontend`) should report **healthy / running**.

---

## Port Mapping & Access URLs

| Interface / Service | URL | Description |
|---|---|---|
| **Citizen Portal** | [http://localhost:5500/](http://localhost:5500/) | Submit grievances with AI category & priority analysis |
| **Officer Dashboard** | [http://localhost:5500/officer/](http://localhost:5500/officer/) | View, filter, and resolve department grievances |
| **Swagger API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive testing for all REST endpoints |
| **Unified Portal** | [http://localhost:8000/](http://localhost:8000/) | Centralized launch dashboard |
| **Health Check** | [http://localhost:8000/health](http://localhost:8000/health) | Live DB connectivity & model status check |

---

## Default Officer Accounts (Pre-Seeded)

All demo officer accounts share the password **`admin123`**:

| Department | Username | Password |
|---|---|---|
| **Municipal** | `municipal_admin` | `admin123` |
| **Water** | `water_admin` | `admin123` |
| **Electricity** | `electricity_admin` | `admin123` |
| **Gas** | `gas_admin` | `admin123` |
| **Transport** | `transport_admin` | `admin123` |

### Test Citizen IDs
Initial pre-registered citizen IDs:
- **`1`** - Naman Sharma (New Delhi)
- **`2`** - Deepanshu Sharma (Mumbai)
- **`3`** - Himani Sharma (Bangalore)
- **`4`** - Piyush Kumar (Bulandshahar)
- **`5`** - Chirag Patel (Ahmedabad)

---

## Stopping & Resetting

To stop containers:
```bash
docker compose down
```

To stop containers and wipe volume data (fresh database):
```bash
docker compose down -v
```
