# Pfumelani Portfolio — Django REST API

Django REST Framework backend for a personal software-development portfolio.

## Approved architecture
- **Database:** PostgreSQL in deployed environments (SQLite is available for local development).
- **Media:** S3-compatible cloud object storage using `django-storages` (AWS S3, Cloudflare R2, or another compatible provider). Keep credentials in environment variables; never commit `.env`.
- **Authentication:** JWT access and refresh tokens using SimpleJWT. Access tokens expire after 15 minutes; refresh tokens after 7 days and rotate on refresh.
- **GitHub:** Live GitHub REST API requests with a five-minute cache and stale-cache fallback for up to 24 hours after upstream errors.
- **Hosting:** React frontend and Django API deployed separately. Configure the frontend origin in `CORS_ALLOWED_ORIGINS`; configure backend `ALLOWED_HOSTS` and HTTPS at deployment.

## Local setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations core projects education blog contact
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Set `DATABASE_URL` to a PostgreSQL connection string when using PostgreSQL. For cloud media, set `USE_S3_MEDIA=True` and configure the S3 environment variables. `AWS_S3_ENDPOINT_URL` is optional for AWS and useful for S3-compatible providers such as Cloudflare R2.

## API v1
| Method | Endpoint | Purpose |
|---|---|---|
| GET/PATCH | `/api/v1/profile/` | Public profile; owner edits with JWT |
| GET/POST | `/api/v1/skills/` | Skills |
| GET/POST | `/api/v1/projects/` | Published projects; owner CRUD |
| GET/POST | `/api/v1/education/` | Education timeline |
| GET/POST | `/api/v1/certificates/` | Published certificates; owner CRUD |
| GET | `/api/v1/resume/` | Active CV metadata and cloud file URL |
| POST | `/api/v1/contact/` | Public contact form submission |
| GET/POST | `/api/v1/blog/posts/` | Published blog posts; owner CRUD |
| GET/POST | `/api/v1/blog/categories/` | Blog categories |
| GET | `/api/v1/github/repositories/` | Live GitHub repositories with caching |
| POST | `/api/v1/auth/token/` | Obtain JWT pair |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token |
| POST | `/api/v1/auth/token/verify/` | Verify token |

The write operations on content endpoints require an authenticated account. Create the portfolio owner using `createsuperuser`; do not expose admin credentials in the frontend. The contact endpoint is intentionally public and rate-limited.

## Frontend integration
The React app should call the API using the deployed backend base URL. Send `Authorization: ****** for protected requests. Keep the refresh token in a secure strategy appropriate to the deployment; for a browser application, prefer an HttpOnly, Secure, SameSite cookie-based refresh flow rather than persistent browser storage. The current SimpleJWT endpoints are a starter token flow and should be wrapped with that cookie strategy before production.

## Important production checklist
- Use PostgreSQL, a strong `SECRET_KEY`, HTTPS, and `DEBUG=False`.
- Restrict CORS to the exact deployed frontend origin(s).
- Configure cloud storage bucket access, CORS, file-size/type validation, and lifecycle/backup policies.
- Configure a shared cache (e.g. Redis) for multi-instance deployments; Django's local-memory cache is not shared between hosts.
- Add automated tests, monitoring, backups, and email delivery/anti-spam controls for contact submissions.
- Run `makemigrations` and review generated migrations before deployment.
