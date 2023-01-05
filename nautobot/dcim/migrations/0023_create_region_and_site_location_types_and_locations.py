# Generated by Django 3.2.16 on 2022-12-23 02:48

from django.db import migrations


def create_region_location_type_locations(region_class, location_class, region_lt):
    """
    Create location objects for each region instance in the region_class model.

    Args:
        region_class: The model class for legacy regions
        location_class: The model class for locations
        region_lt: The newly created region location type
    """
    # Breadth First Query to create parents on the top levels first and children second.
    regions = region_class.objects.with_tree_fields().extra(order_by=["__tree.tree_depth", "__tree.tree_ordering"])
    for region in regions:
        location_class.objects.create(
            location_type=region_lt,
            name=region.name,
            description=region.description,
            parent=location_class.objects.get(name=region.parent.name, location_type=region_lt)
            if region.parent
            else None,
        )


def create_site_location_type_locations(
    site_class,
    location_type_class,
    location_class,
    site_lt,
    exclude_name,
    has_parent_location=False,
    region_lt=None,
):
    """
    Create location objects for each site instance in the site_class model.

    Args:
        site_class: The model class for Legacy sites
        location_type_class: The model class for location types
        location_class: The model class for locations
        site_lt: The newly created site location type
        exclude_name: The name to exclude from the update query
        has_parent_location: Whether the newly created site location has a parent location or not
        region_lt: The newly created region location type, required if has_parent_location
    """

    location_instances = []
    for site in site_class.objects.all():
        extra_kwargs = {}

        if has_parent_location:
            extra_kwargs["parent"] = location_class.objects.get(
                location_type=region_lt, name=site.region.name if site.region else "Global Region"
            )
        location_instances.append(
            location_class(
                name=site.name,
                location_type=site_lt,
                tenant=site.tenant,
                facility=site.facility,
                asn=site.asn,
                time_zone=site.time_zone,
                description=site.description,
                physical_address=site.physical_address,
                shipping_address=site.shipping_address,
                latitude=site.latitude,
                longitude=site.longitude,
                contact_name=site.contact_name,
                contact_phone=site.contact_phone,
                contact_email=site.contact_email,
                comments=site.comments,
                status=site.status,
                tags=site.tags,
                **extra_kwargs,
            )
        )
    location_class.objects.bulk_create(location_instances, batch_size=1000)
    # Set existing top level locations to have site locations as their parents
    for location in location_class.objects.filter(site__isnull=False):
        location.parent = location_class.objects.get(name=location.site.name, location_type=site_lt)
        location.save()
    location_type_class.objects.filter(parent__isnull=True).exclude(name=exclude_name).update(parent=site_lt)


def migrate_site_and_region_data_to_locations(apps, schema_editor):
    """
    Create Location objects based on existing data and move Site related objects to be associated with new Location objects.
    """
    Region = apps.get_model("dcim", "region")
    Site = apps.get_model("dcim", "site")
    LocationType = apps.get_model("dcim", "locationtype")
    Location = apps.get_model("dcim", "location")

    # Region instances exist
    if Region.objects.exists():
        region_lt = LocationType.objects.create(name="Region", nestable=True)
        create_region_location_type_locations(region_class=Region, location_class=Location, region_lt=region_lt)
        if Site.objects.exists():  # Both Site and Region instances exist
            site_lt = LocationType.objects.create(name="Site", parent=LocationType.objects.get(name="Region"))
            if Site.objects.filter(region__isnull=True).exists():
                Location.objects.create(
                    location_type=region_lt,
                    name="Global Region",
                    description="Parent Location of Region LocationType for all sites that "
                    "did not have a region attribute set before the migration",
                )
            create_site_location_type_locations(
                site_class=Site,
                location_type_class=LocationType,
                location_class=Location,
                site_lt=site_lt,
                exclude_name="Region",
                has_parent_location=True,
                region_lt=region_lt,
            )
    elif Site.objects.exists():  # Only Site instances exist, we make Site the top level LocationType
        site_lt = LocationType.objects.create(name="Site")
        create_site_location_type_locations(
            site_class=Region,
            location_type_class=LocationType,
            location_class=Location,
            site_lt=site_lt,
            exclude_name="Site",
        )

    # Reassign Site Models to Locations of Site LocationType
    if Site.objects.exists():  # Iff Site instances exist
        CircuitTermination = apps.get_model("circuits", "circuittermination")
        Device = apps.get_model("dcim", "device")
        PowerPanel = apps.get_model("dcim", "powerpanel")
        RackGroup = apps.get_model("dcim", "rackgroup")
        Rack = apps.get_model("dcim", "rack")
        Prefix = apps.get_model("ipam", "prefix")
        VLANGroup = apps.get_model("ipam", "vlangroup")
        VLAN = apps.get_model("ipam", "vlan")
        Cluster = apps.get_model("virtualization", "cluster")

        for ct in CircuitTermination.objects.filter(location__isnull=True):
            ct.location = Location.objects.get(name=ct.site.name, location_type=site_lt)
            ct.save()
        for device in Device.objects.filter(location__isnull=True):
            device.location = Location.objects.get(name=device.site.name, location_type=site_lt)
            device.save()
        for powerpanel in PowerPanel.objects.filter(location__isnull=True):
            powerpanel.location = Location.objects.get(name=powerpanel.site.name, location_type=site_lt)
            powerpanel.save()
        for rackgroup in RackGroup.objects.filter(location__isnull=True):
            rackgroup.location = Location.objects.get(name=rackgroup.site.name, location_type=site_lt)
            rackgroup.save()
        for rack in Rack.objects.filter(location__isnull=True):
            rack.location = Location.objects.get(name=rack.site.name, location_type=site_lt)
            rack.save()
        # Below models' site attribute is not required, so we need to check each instance if the site field is not null
        # if so we reassign it to Site Location and if not we leave it alone
        for prefix in Prefix.objects.filter(location__isnull=True, site__isnull=False):
            prefix.location = Location.objects.get(name=prefix.site.name, location_type=site_lt)
            prefix.save()
        for vlangroup in VLANGroup.objects.filter(location__isnull=True, site__isnull=False):
            vlangroup.location = Location.objects.get(name=vlangroup.site.name, location_type=site_lt)
            vlangroup.save()
        for vlan in VLAN.objects.filter(location__isnull=True, site__isnull=False):
            vlan.location = Location.objects.get(name=vlan.site.name, location_type=site_lt)
            vlan.save()
        for cluster in Cluster.objects.filter(location__isnull=True, site__isnull=False):
            cluster.location = Location.objects.get(name=cluster.site.name, location_type=site_lt)
            cluster.save()


class Migration(migrations.Migration):

    dependencies = [
        ("dcim", "0022_change_tree_manager_on_tree_models"),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_site_and_region_data_to_locations,
            reverse_code=migrations.operations.special.RunPython.noop,
        ),
    ]
