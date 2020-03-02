# Generated by Django 2.2.8 on 2019-12-05 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0004_auto_20191013_1053"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message", options={"ordering": ["timestamp"]},
        ),
        migrations.AlterField(
            model_name="chat",
            name="turker",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
