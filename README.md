# Distributed Task Scheduling & Notification Microservice Engine

A highly scalable, containerized distributed notification engine built with **Django REST Framework**, **PostgreSQL**, **Redis**, and **Celery**. This system features timezone-accurate temporal scheduling buffers and secure JWT authentication routing, optimized to bypass consumer network limitations using secure production SMTP/SSL channels.

##  System Architecture Topology

The application runs as an orchestrated multi-container cluster inside an isolated virtual network bridge:

* **Django REST Framework API Gateway (Port 8000):** Secure, token-fortified entry point managing validations and access controls.
* **PostgreSQL Database Core (Port 5432):** Long-term persistent relational data storage tracking operational states.
* **Redis Message Queue Broker (Port 6379):** High-speed system RAM transit queue load-balancing task tickets.
* **Celery Beat Conductor:** Timezone-synchronized clock daemon scanning database targets periodically.
* **Celery Worker Pool:** Computational heavy-lifting thread pool managing production encrypted network SMTP connection streams.

---

##  Quick Start with Docker Compose

Ensure you have **Docker** and **Docker Compose V2** installed natively on your host machine.

### 1. Environment Configurations
Clone the project repository and create a local hidden configuration file named `.env` in the root workspace:

```ini
DEBUG=True
SECRET_KEY=your_runtime_cryptographic_secret_key

DB_NAME=notification_db
DB_USER=notification_user
DB_PASSWORD=ayodeji0
DB_HOST=postgres_db
DB_PORT=5432

CELERY_BROKER_URL=redis://redis_queue:6379/0
CELERY_RESULT_BACKEND=redis://redis_queue:6379/0

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=://gmail.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_USE_TLS=False
EMAIL_HOST_USER=your_verified_gmail_address@gmail.com
EMAIL_HOST_PASSWORD=your_16_character_google_app_password
```

### 2. Orchestrate and Spin Up the Cluster
Launch all 5 infrastructure layers concurrently inside a synchronized background thread matrix:

```bash
docker compose up -d
```

### 3. Run Database Schema Migrations
Command Docker to execute database initialization schemas straight inside the isolated PostgreSQL container box:

```bash
docker compose exec web_api python manage.py migrate
```

### 4. Create Administrative Control Profile
```bash
docker compose exec web_api python manage.py createsuperuser
```

### 5. Initialize the Temporal Timer Clock
1. Navigate to the web gateway admin page at `http://127.0.0`.
2. Under the **Django Celery Beat** workspace, navigate to **Intervals** and add a `10 Seconds` rhythm slot.
3. Move to **Periodic Tasks**, register a new task row pointing to `notifications.tasks.check_and_dispatch_scheduled_notifications`, and mount the 10-second interval rule.

---

##  API Authentication & Resource Gateways

###  1. Fetch Cryptographic Access Tokens
* **Method:** `POST`
* **Route:** `/api/v1/auth/login/`
* **Payload:**
```json
{
  "username": "your_superuser_name",
  "password": "your_superuser_password"
}
```

###  2. Dispatch a Scheduled Notification Job
* **Method:** `POST`
* **Route:** `/api/v1/jobs/`
* **Header:** `Authorization: Bearer <your_access_token_string>`
* **Payload:** *(Ensure timestamps use explicit Zulu/UTC syntax notation)*
```json
{
  "title": "The Container Symphony!",
  "message": "Distributed microservice successfully deployed!",
  "recipient_email": "target_inbox@gmail.com",
  "scheduled_time": "2026-08-17T16:00:00Z"
}
```

---

##  Infrastructure Maintenance Controls

* **Graceful Stand-Down (Preserves Data Volumes):** `docker compose down`
* **Hard-Reset Reset (Wipes All Cached State Data):** `docker compose down -v`
