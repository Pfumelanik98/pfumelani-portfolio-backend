# Technical design decisions and API contract

## Deployment topology
React SPA is hosted independently from the Django REST API. PostgreSQL is the managed relational database. Uploaded profile images, project screenshots, certificates, and CV files are stored in S3-compatible object storage; only object keys/metadata are stored in PostgreSQL. The frontend accesses media through the storage URL returned by Django.

## Security boundaries
JWT is required for content writes and owner operations. Public visitors can read published portfolio content and submit contact messages. Draft/unpublished content is excluded from anonymous querysets. The contact endpoint is anonymous by design and throttled. Do not create a public registration endpoint for the single-owner portfolio.

## Domain model
- `Profile`: public owner profile and social/contact links.
- `Skill`: categorized skill catalogue; projects relate through `ProjectTechnology`.
- `Project`: portfolio project with publication/featured state and ordered `ProjectImage` gallery.
- `Education`: qualification timeline.
- `Certificate`: issuer, issue date, verification URL and optional cloud document.
- `Resume`: uploaded CV; only one record should be active at a time.
- `BlogCategory`, `BlogPost`: categorized technical articles with draft/published state.
- `ContactMessage`: inbound enquiries and owner-managed status.

## Initial response conventions
List endpoints return DRf paginated responses when pagination is configured by deployment. Image/File fields serialize to their cloud URLs. Project detail lookup uses `slug`; blog detail lookup uses the default primary key in this initial version unless `lookup_field = "slug"` is added to its viewset.
