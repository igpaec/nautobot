# Generated by Django 3.2.16 on 2022-11-23 12:27

from django.db import migrations
import django.db.models.deletion
import nautobot.extras.models.roles


class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0055_collect_roles_from_related_apps_roles"),
        ("virtualization", "0009_cluster_location"),
    ]

    operations = [
        migrations.RenameField(
            model_name="virtualmachine",
            old_name="role",
            new_name="legacy_role",
        ),
        migrations.AddField(
            model_name="virtualmachine",
            name="new_role",
            field=nautobot.extras.models.roles.RoleField(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="virtualization_virtualmachine_related",
                to="extras.role",
            ),
        ),
    ]
