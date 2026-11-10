# Pfumelani Portfolio Backend

Django REST Framework backend starter for a professional developer portfolio.

## Technology
- Python and Django
- Django REST Framework
- PostgreSQL (configured through `DATABASE_URL`)
- JWT authentication

## Project setup

1. Download and extract the backend starter ZIP supplied with this project.
2. Copy the extracted project files into this repository's root folder.
3. Create and activate a Python virtual environment.
4. Install dependencies with `pip install -r requirements.txt`.
5. Copy `.env.example` to `.env` and configure your database settings.
6. Generate and apply migrations:

```bash
python manage.py makemigrations core projects education blog contact
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The Django admin is available at `/admin/`. API routes are defined in the project URL configuration.

## Important
This is a starter scaffold, not a production deployment. Review environment settings, authentication, permissions, validation, tests, and deployment configuration before publishing a live service. Never commit `.env`, passwords, API keys, or other secrets.
