# Generated by Django 3.2.16 on 2022-11-25 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0060_configcontext_data_migrations"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="configcontext",
            name="legacy_roles",
        ),
        migrations.RenameField(
            model_name="configcontext",
            old_name="new_roles",
            new_name="roles",
        ),
    ]
