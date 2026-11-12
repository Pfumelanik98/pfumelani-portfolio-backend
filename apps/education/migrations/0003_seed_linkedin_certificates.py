from datetime import date

from django.db import migrations


CERTIFICATES = [
    {
        "title": "GenAI Course for Software Engineers",
        "issuer": "WeThinkCode",
        "issue_date": date(2026, 8, 1),
        "expiration_date": date(2036, 9, 1),
        "credential_id": "Pfumelani Rikhotso",
        "skills": [],
    },
    {
        "title": "Career Management Essentials",
        "issuer": "IBM",
        "issue_date": date(2026, 5, 1),
        "expiration_date": date(2036, 1, 1),
        "skills": ["Social Media", "Generative Ai tool"],
    },
    {
        "title": "Working in a Digital World: Professional Skills",
        "issuer": "IBM",
        "issue_date": date(2024, 6, 1),
        "expiration_date": date(2035, 7, 1),
        "skills": ["Team Collaboration", "Creativity and Innovation"],
    },
    {
        "title": "Introduction to Cybersecurity",
        "issuer": "Cisco",
        "issue_date": date(2026, 5, 1),
        "expiration_date": date(2036, 6, 1),
        "credential_id": "Pfumelani Rikhotso",
        "skills": ["Cyberlaw", "Cyber Threat Intelligence (CTI)"],
    },
    {
        "title": "CCNA: Switching, Routing, and Wireless Essentials",
        "issuer": "Cisco",
        "issue_date": date(2022, 6, 1),
        "skills": [],
    },
    {
        "title": "AWS Educate Getting Started with Compute",
        "issuer": "Amazon Web Services (AWS)",
        "issue_date": date(2023, 10, 1),
        "skills": [],
    },
    {
        "title": "AWS Educate Getting Started with Serverless",
        "issuer": "Amazon Web Services (AWS)",
        "issue_date": date(2023, 10, 1),
        "skills": [],
    },
    {
        "title": "AWS Educate Getting Started with Cloud Ops",
        "issuer": "Amazon Web Services (AWS)",
        "issue_date": date(2023, 10, 1),
        "skills": [],
    },
    {
        "title": "AWS Educate Introduction to Cloud 101",
        "issuer": "Amazon Web Services (AWS)",
        "issue_date": date(2023, 10, 1),
        "skills": [],
    },
    {
        "title": "AWS Educate Machine Learning - DeepRacer",
        "issuer": "Amazon Web Services (AWS)",
        "issue_date": date(2023, 10, 1),
        "skills": [],
    },
    {
        "title": "AWS Educate Machine Learning Foundations",
        "issuer": "Amazon Web Services (AWS)",
        "issue_date": date(2023, 10, 1),
        "skills": [],
    },
    {
        "title": "AWS Educate Getting Started with Security",
        "issuer": "Amazon Web Services (AWS)",
        "issue_date": date(2023, 11, 1),
        "skills": [],
    },
    {
        "title": "AWS Educate Web Builder",
        "issuer": "Amazon Web Services (AWS)",
        "issue_date": date(2023, 11, 1),
        "skills": [],
    },
]


def seed_certificates(apps, schema_editor):
    Certificate = apps.get_model("education", "Certificate")
    manager = Certificate.objects.using(schema_editor.connection.alias)

    for certificate in CERTIFICATES:
        title = certificate["title"]
        issuer = certificate["issuer"]
        values = {key: value for key, value in certificate.items() if key not in {"title", "issuer"}}
        values["is_published"] = True
        record, created = manager.get_or_create(
            title=title,
            issuer=issuer,
            defaults=values,
        )
        if not created:
            manager.filter(pk=record.pk).update(**values)


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0002_certificate_credential_id_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_certificates, migrations.RunPython.noop),
    ]
