# Generated by Django 3.2.16 on 2022-12-15 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dcim", "0020_move_site_fields_to_location_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inventoryitem",
            name="level",
        ),
        migrations.RemoveField(
            model_name="inventoryitem",
            name="lft",
        ),
        migrations.RemoveField(
            model_name="inventoryitem",
            name="rght",
        ),
        migrations.RemoveField(
            model_name="inventoryitem",
            name="tree_id",
        ),
        migrations.RemoveField(
            model_name="rackgroup",
            name="level",
        ),
        migrations.RemoveField(
            model_name="rackgroup",
            name="lft",
        ),
        migrations.RemoveField(
            model_name="rackgroup",
            name="rght",
        ),
        migrations.RemoveField(
            model_name="rackgroup",
            name="tree_id",
        ),
        migrations.RemoveField(
            model_name="region",
            name="level",
        ),
        migrations.RemoveField(
            model_name="region",
            name="lft",
        ),
        migrations.RemoveField(
            model_name="region",
            name="rght",
        ),
        migrations.RemoveField(
            model_name="region",
            name="tree_id",
        ),
        migrations.AlterField(
            model_name="inventoryitem",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="dcim.inventoryitem",
            ),
        ),
        migrations.AlterField(
            model_name="rackgroup",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="dcim.rackgroup",
            ),
        ),
        migrations.AlterField(
            model_name="region",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="dcim.region",
            ),
        ),
        migrations.AlterModelOptions(
            name="inventoryitem",
            options={"ordering": ("_name",)},
        ),
        migrations.AlterModelOptions(
            name="rackgroup",
            options={"ordering": ("name",)},
        ),
        migrations.AlterModelOptions(
            name="region",
            options={"ordering": ("name",)},
        ),
    ]
