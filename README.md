EduTrack is a course management web application built with Django and deployed using a production-style Docker multi-container architecture.
The project demonstrates containerization, reverse proxy configuration, security hardening, and deployment best practices for Distributed Systems and Cloud Computing coursework.

TECH STACK

Django 6
PostgreSQL 16
Gunicorn (WSGI server)
Nginx (reverse proxy)
Docker (multi-stage build)
Docker Compose (multi-container orchestration)

ARCHITECTURE

User
→ Nginx (Reverse Proxy)
→ Gunicorn (Django Application)
→ PostgreSQL Database

Services:
db: PostgreSQL database container
web: Django application served by Gunicorn
nginx: Reverse proxy and static/media file server

FEATURES

User authentication
Role-based access (students / instructors)
Course creation and enrollment
Lesson video uploads
Assignment submission system
Instructor grading panel
Health check endpoint
Production-ready Docker deployment
Static and media file separation
Security headers and rate limiting

SECURITY HARDENING

The application includes:
Non-root Docker user
Django SecurityMiddleware enabled
Login rate limiting via Nginx
X-Frame-Options protection
Content-Security-Policy headers
MIME sniffing protection
Secure referrer policy
Environment variable based secrets
Static files served by Nginx
Separate production settings
Gunicorn instead of Django development server

DOCKER DEPLOYMENT

Build and run the system:
docker-compose up -d --build
Stop the system:
docker-compose down

ACCESS POINTS

Application: http://localhost
Login: http://localhost/login/
Admin panel: http://localhost/admin/
Health check: http://localhost/health/
The health endpoint returns: {"status": "ok"}

ENVIRONMENT VARIABLES

The project uses a .env file (not committed to Git).
Required variables:
SECRET_KEY
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DJANGO_SETTINGS_MODULE

PRODUCTION DESIGN DECISIONS

Multi-stage Docker build to reduce image size
Gunicorn used as WSGI server
Nginx reverse proxy for performance and security
Persistent PostgreSQL volume
Static files collected during image build
Environment-specific Django settings
No secrets stored in the repository

DOCKER HUB IMAGE

The production image is available on Docker Hub:
docker pull 00015850/edutrack-web:v4

COURSEWORK COVERAGE

Completed:
Multi-container Docker setup
Docker Compose orchestration
Reverse proxy with Nginx
Gunicorn production deployment
Security hardening
Health monitoring endpoint
Git history preservation
Branch and pull request workflow
Cloud VM deployment (Azure)
SSH access configuration

NOTES

HTTPS can be enabled later using Nginx SSL configuration.
Database data is stored in Docker volumes and is not included in Docker images.
The system is designed to be portable and reproducible across environments.

LICENSE

Educational use only.