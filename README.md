# Django Asynchronous Periodic Tasks with Celery Beat, Redis & Docker

<div align="center">

[![GitHub Release](https://img.shields.io/github/v/release/codewithmuh/celery-beat?color=blue&logo=github)](https://github.com/codewithmuh/celery-beat/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/codewithmuh/celery-beat?style=flat&color=gold)](https://github.com/codewithmuh/celery-beat/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/codewithmuh/celery-beat?style=flat&color=teal)](https://github.com/codewithmuh/celery-beat/network/members)
[![Django](https://img.shields.io/badge/Backend-Django_4.x-092E20?logo=django)](https://www.djangoproject.com/)
[![Celery](https://img.shields.io/badge/Task_Queue-Celery_|_Beat-37814A?logo=celery)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Broker-Redis_Alpine-DC382D?logo=redis)](https://redis.io/)
[![Docker Compose](https://img.shields.io/badge/Container-Docker_Compose-2496ED?logo=docker)](https://www.docker.com/)
[![YouTube: @codewithmuh](https://img.shields.io/badge/YouTube-codewithmuh-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/@codewithmuh)

**A complete, production-ready blueprint for orchestrating automated periodic background tasks and asynchronous job queues in Django using Celery Beat, Redis, and multi-container Docker Compose.**

[Overview](#overview) • [Architecture](#system-architecture) • [Features](#key-features) • [Quick Start](#quick-start-guide) • [Management Commands](#management-commands--testing) • [Container Stack](#docker-compose-services)

</div>

---

## Overview

In modern web development, time-consuming operations—such as compiling daily sales summaries, synchronizing order inventories, and dispatching customer notification emails—should never block synchronous HTTP request cycles. 

**`celery-beat`** provides a turnkey multi-container architecture demonstrating how to combine **Django**, **Celery Workers**, **Celery Beat (Periodic Scheduler)**, and an in-memory **Redis** message broker to schedule and execute background tasks reliably.

---

## System Architecture

```mermaid
flowchart TD
    subgraph Schedulers["Periodic Task Scheduler"]
        Beat["Celery Beat Daemon (crontab / intervals)"]
    end

    subgraph Broker["Message Transport"]
        Redis[("Redis In-Memory Broker (redis:alpine)")]
    end

    subgraph Workers["Distributed Execution Pool"]
        Worker1["Celery Worker Node 1"]
        Worker2["Celery Worker Node 2"]
    end

    subgraph DjangoApp["Web Application & Database"]
        Web["Django Web Server (Port 8090)"]
        DB[("PostgreSQL / SQLite Database")]
        Email["SMTP Email Dispatcher"]
    end

    Beat -->|1. Dispatches Scheduled Job| Redis
    Web -->|Ad-Hoc Async Task .delay()| Redis
    Redis -->|2. Pulls Task from Queue| Worker1 & Worker2
    Worker1 & Worker2 -->|3. Processes Job & Updates State| DB
    Worker1 & Worker2 -->|4. Sends Automated Reports| Email
```

---

## Key Features

- **Automated Periodic Scheduling:** Configured with Celery Beat to execute background tasks on crontab intervals without requiring Linux system crontabs.
- **Asynchronous Order Processing:** Example e-commerce `orders` application processing products, inventory calculations, and data seeding.
- **Docker Compose Multi-Service Architecture:** Orchestrates 4 independent containers (`web`, `redis`, `celery`, `celery-beat`) with isolated networking and health dependencies.
- **Custom Management Commands:** Pre-built Django CLI commands for manual testing, bulk data fixture loading, and scheduled email report triggers.

---

## Docker Compose Services

| Service | Image / Build | Port | Role & Responsibility |
|---|---|:---:|---|
| **`web`** | `python:3.10-slim` | `8090:8000` | Django web application backend handling HTTP requests and admin portal. |
| **`redis`** | `redis:alpine` | Internal `6379` | In-memory message broker coordinating task queues between producer and workers. |
| **`celery`** | `python:3.10-slim` | Internal | Background distributed worker pool executing queued tasks (`celery -A core worker`). |
| **`celery-beat`** | `python:3.10-slim` | Internal | Clock daemon dispatching periodic recurring tasks into Redis (`celery -A core beat`). |

---

## Quick Start Guide

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.

### 1. Build and Launch Containers

```bash
git clone https://github.com/codewithmuh/celery-beat.git
cd celery-beat

# Build and start all 4 services in detached mode
docker compose up -d --build
```

### 2. Run Database Migrations & Load Data Fixtures

Seed sample product catalog items:

```bash
# Apply Django migrations
docker compose exec web python manage.py migrate

# Load initial product fixtures
docker compose exec web python manage.py loaddata products.json
```

### 3. Verify Container Health

```bash
docker compose ps
```

Visit the Django web application at `http://localhost:8090`.

---

## Management Commands & Testing

Trigger background tasks and custom scripts directly inside the container environment:

```bash
# Execute custom background batch command
docker compose exec web python manage.py my_custom_command

# Trigger on-demand email summary report
docker compose exec web python manage.py email_report
```

### Monitoring Celery Worker & Beat Logs

Inspect real-time task ingestion and scheduling:

```bash
# Follow Celery Worker task execution logs
docker compose logs -f celery

# Follow Celery Beat scheduler dispatch logs
docker compose logs -f celery-beat
```

### Stopping the Stack

```bash
docker compose down
```

---

## Project Structure

```
celery-beat/
├── Dockerfile              # Python 3.10 slim environment container definition
├── docker-compose.yml      # Orchestration for web, redis, celery, celery-beat
├── entrypoint.sh           # Migration and startup orchestration script
├── manage.py               # Django CLI management utility
├── products.json           # Sample initial product fixtures
├── requirements.txt        # Python package dependencies (Django, Celery, Redis)
├── core/                   # Core Django project settings & celery.py config
│   ├── __init__.py         # Celery app registration
│   ├── celery.py           # Celery instance & beat schedule definitions
│   ├── settings.py         # Broker URLs, installed apps, timezone
│   └── urls.py             # Root URL routing
└── orders/                 # Sample application with models & tasks
    ├── models.py           # Product & Order data models
    ├── tasks.py            # Celery @shared_task definitions
    └── management/         # Custom CLI testing commands
```

---

## Community & Resources

- 🌐 **DevOps Training Hub:** [devops-training-resources](https://github.com/codewithmuh/devops-training-resources)
- 📺 **YouTube Channel:** [CodeWithMuh](https://www.youtube.com/@codewithmuh)
- 👤 **Follow on LinkedIn:** [Muhammad Rashid](https://www.linkedin.com/in/codewithmuh)

---

## License

This project is licensed under the [MIT License](LICENSE).
