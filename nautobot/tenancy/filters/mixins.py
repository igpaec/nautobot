import django_filters

from nautobot.tenancy.models import Tenant, TenantGroup
from nautobot.utilities.filters import NaturalKeyOrPKMultipleChoiceFilter, TreeNodeMultipleChoiceFilter


class TenancyModelFilterSetMixin(django_filters.FilterSet):
    """
    An inheritable FilterSet for models which support Tenant assignment.
    """

    tenant_group = TreeNodeMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        field_name="tenant__tenant_group",
        to_field_name="slug",
        label="Tenant Group (slug or ID)",
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label='Tenant (ID) (deprecated, use "tenant" filter instead)',
    )
    tenant = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label="Tenant (slug or ID)",
    )
