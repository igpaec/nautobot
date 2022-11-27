# Generated by Django 3.2.16 on 2022-11-23 12:27

from django.db import migrations
from nautobot.extras.utils import migrate_role_data
from nautobot.ipam.choices import IPAddressRoleChoices


def migrate_data_from_legacy_role_to_new_role(apps, schema):
    """Copy record from role to temp_role"""

    role_model = apps.get_model("extras", "Role")
    model_class_is_choice_field_map = {
        "VLAN": False,
        "Prefix": False,
        "IPAddress": True,
    }
    for model_name, is_choices in model_class_is_choice_field_map.items():
        model = apps.get_model("ipam", model_name)
        migrate_role_data(model=model, role_model=role_model, is_choice_field=is_choices)


def reverse_role_data_migrate(apps, schema):
    """Reverse changes made to new_role"""

    model_role_map = {
        "VLAN": {"role_model": "Role"},
        "Prefix": {"role_model": "Role"},
        "IPAddress": {"role_choiceset": IPAddressRoleChoices},
    }
    for model_name, value in model_role_map.items():
        role_model = None
        role_choiceset = None
        model = apps.get_model("ipam", model_name)
        if "role_model" in value:
            role_model = apps.get_model("ipam", value["role_model"])
        else:
            role_choiceset = value["role_choiceset"]
        migrate_role_data(
            model=model,
            role_model=role_model,
            role_choiceset=role_choiceset,
            legacy_role="new_role",
            new_role="legacy_role",
        )


class Migration(migrations.Migration):

    dependencies = [
        ("ipam", "0009_alter_ipam_role_add_new_role"),
    ]

    operations = [
        migrations.RunPython(migrate_data_from_legacy_role_to_new_role, reverse_role_data_migrate),
    ]
