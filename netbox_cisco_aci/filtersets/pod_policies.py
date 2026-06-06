"""FilterSets for the pod-policy family."""

import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ..choices import (
    EnabledDisabledChoices,
    NTPProviderStateChoices,
    SNMPAuthProtocolChoices,
    SNMPPrivProtocolChoices,
    SNMPVersionChoices,
    SyslogFacilityChoices,
    SyslogSeverityChoices,
)
from ..models.fabric import ACIFabric
from ..models.pod_policies import (
    ACINTPPolicy,
    ACINTPProvider,
    ACIPodPolicyGroup,
    ACISNMPClient,
    ACISNMPClientGroup,
    ACISNMPCommunity,
    ACISNMPPolicy,
    ACISNMPTrapDest,
    ACISNMPTrapPolicy,
    ACISNMPv3User,
    ACISyslogPolicy,
    ACISyslogRemoteDest,
)
from ..models.tenant import ACITenant


def _q_name(value):
    return (
        Q(name__icontains=value) | Q(name_alias__icontains=value) | Q(description__icontains=value)
    )


# ---------------------------------------------------------------------------
# NTP
# ---------------------------------------------------------------------------


class ACINTPPolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    admin_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)

    class Meta:
        model = ACINTPPolicy
        fields = ("id", "name", "name_alias", "description", "auth_state")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(_q_name(value))


class ACINTPProviderFilterSet(NetBoxModelFilterSet):
    ntp_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACINTPPolicy.objects.all(), field_name="ntp_policy", label="NTP Policy (ID)"
    )
    role = django_filters.MultipleChoiceFilter(choices=NTPProviderStateChoices)

    class Meta:
        model = ACINTPProvider
        fields = ("id", "name", "host", "key_id", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(host__icontains=value) | Q(description__icontains=value)
        )


# ---------------------------------------------------------------------------
# Syslog
# ---------------------------------------------------------------------------


class ACISyslogPolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    admin_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)
    console_severity = django_filters.MultipleChoiceFilter(choices=SyslogSeverityChoices)
    local_severity = django_filters.MultipleChoiceFilter(choices=SyslogSeverityChoices)

    class Meta:
        model = ACISyslogPolicy
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(_q_name(value))


class ACISyslogRemoteDestFilterSet(NetBoxModelFilterSet):
    syslog_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISyslogPolicy.objects.all(),
        field_name="syslog_policy",
        label="Syslog Policy (ID)",
    )
    severity = django_filters.MultipleChoiceFilter(choices=SyslogSeverityChoices)
    forwarding_facility = django_filters.MultipleChoiceFilter(choices=SyslogFacilityChoices)
    admin_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)

    class Meta:
        model = ACISyslogRemoteDest
        fields = ("id", "name", "host", "port", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(host__icontains=value) | Q(description__icontains=value)
        )


# ---------------------------------------------------------------------------
# SNMP
# ---------------------------------------------------------------------------


class ACISNMPPolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    admin_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)

    class Meta:
        model = ACISNMPPolicy
        fields = ("id", "name", "name_alias", "description", "contact", "location")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            _q_name(value) | Q(contact__icontains=value) | Q(location__icontains=value)
        )


class ACISNMPCommunityFilterSet(NetBoxModelFilterSet):
    snmp_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISNMPPolicy.objects.all(), field_name="snmp_policy", label="SNMP Policy (ID)"
    )

    class Meta:
        model = ACISNMPCommunity
        fields = ("id", "name", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(_q_name(value))


class ACISNMPClientGroupFilterSet(NetBoxModelFilterSet):
    snmp_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISNMPPolicy.objects.all(), field_name="snmp_policy", label="SNMP Policy (ID)"
    )

    class Meta:
        model = ACISNMPClientGroup
        fields = ("id", "name", "description", "mgmt_epg")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(_q_name(value) | Q(mgmt_epg__icontains=value))


class ACISNMPClientFilterSet(NetBoxModelFilterSet):
    client_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISNMPClientGroup.objects.all(),
        field_name="client_group",
        label="Client Group (ID)",
    )

    class Meta:
        model = ACISNMPClient
        fields = ("id", "name", "address", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(address__icontains=value) | Q(description__icontains=value)
        )


class ACISNMPv3UserFilterSet(NetBoxModelFilterSet):
    snmp_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISNMPPolicy.objects.all(), field_name="snmp_policy", label="SNMP Policy (ID)"
    )
    auth_protocol = django_filters.MultipleChoiceFilter(choices=SNMPAuthProtocolChoices)
    privacy_protocol = django_filters.MultipleChoiceFilter(choices=SNMPPrivProtocolChoices)

    class Meta:
        model = ACISNMPv3User
        fields = ("id", "name", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(_q_name(value))


# ---------------------------------------------------------------------------
# SNMP Traps
# ---------------------------------------------------------------------------


class ACISNMPTrapPolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    admin_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)

    class Meta:
        model = ACISNMPTrapPolicy
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(_q_name(value))


class ACISNMPTrapDestFilterSet(NetBoxModelFilterSet):
    trap_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISNMPTrapPolicy.objects.all(),
        field_name="trap_policy",
        label="Trap Policy (ID)",
    )
    version = django_filters.MultipleChoiceFilter(choices=SNMPVersionChoices)

    class Meta:
        model = ACISNMPTrapDest
        fields = ("id", "name", "host", "port", "community_or_user", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(host__icontains=value)
            | Q(community_or_user__icontains=value)
            | Q(description__icontains=value)
        )


# ---------------------------------------------------------------------------
# Pod Policy Group
# ---------------------------------------------------------------------------


class ACIPodPolicyGroupFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    ntp_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACINTPPolicy.objects.all(), field_name="ntp_policy", label="NTP Policy (ID)"
    )
    syslog_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISyslogPolicy.objects.all(),
        field_name="syslog_policy",
        label="Syslog Policy (ID)",
    )
    snmp_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISNMPPolicy.objects.all(), field_name="snmp_policy", label="SNMP Policy (ID)"
    )
    snmp_trap_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISNMPTrapPolicy.objects.all(),
        field_name="snmp_trap_policy",
        label="SNMP Trap Policy (ID)",
    )

    class Meta:
        model = ACIPodPolicyGroup
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(_q_name(value))
