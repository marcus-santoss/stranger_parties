# Generated by Django 3.2.4 on 2021-07-30 02:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=80)),
                ("date_time", models.DateTimeField(null=True)),
            ],
            options={"ordering": ["id", "created_at", "updated_at"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Guest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=80)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=15)),
            ],
            options={"ordering": ["id", "created_at", "updated_at"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Invite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("key", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("confirmed", models.BooleanField(default=False)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guest_invitations",
                        to="invite.event",
                    ),
                ),
                (
                    "guest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_invitations",
                        to="invite.guest",
                    ),
                ),
            ],
            options={"unique_together": {("guest", "event")}},
        ),
    ]
