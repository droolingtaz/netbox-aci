"""Forms for the pod-policy family (NTP / Syslog / SNMP / SNMP Traps).

Each of the twelve pod-policy models gets the standard four-form quartet:
``Form``, ``BulkEditForm``, ``FilterForm``, and ``ImportForm``. The
quartets share enough structure that we keep them all in one module
rather than splitting per-protocol — every form sits next to the ones
it references via ``DynamicModelChoiceField``.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField

from ..choices import (
    EnabledDisabledChoices,
    NTPProviderStateChoices,
    SNMPAuthProtocolChoices,
    SNMPPrivProtocolChoices,
    SNMPSecurityLevelChoices,
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

# ---------------------------------------------------------------------------
# Shared filter-form fragments
# ---------------------------------------------------------------------------


def _fabric_filter_field():
    return DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )


def _tenant_filter_field():
    return DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )


# ===========================================================================
# NTP Policy
# ===========================================================================


class ACINTPPolicyForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    aci_tenant = DynamicModelChoiceField(
        queryset=ACITenant.objects.all(),
        required=False,
        label=_("Tenant"),
        query_params={"aci_fabric_id": "$aci_fabric"},
    )

    class Meta:
        model = ACINTPPolicy
        fields = (
            "aci_fabric",
            "aci_tenant",
            "name",
            "name_alias",
            "admin_state",
            "server_state_default",
            "auth_state",
            "description",
            "tags",
        )


class ACINTPPolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACINTPPolicy
    admin_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    server_state_default = forms.ChoiceField(choices=NTPProviderStateChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "aci_tenant")


class ACINTPPolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACINTPPolicy
    aci_fabric_id = _fabric_filter_field()
    aci_tenant_id = _tenant_filter_field()
    admin_state = forms.MultipleChoiceField(choices=EnabledDisabledChoices, required=False)


class ACINTPPolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")
    aci_tenant = forms.ModelChoiceField(
        queryset=ACITenant.objects.all(), to_field_name="name", required=False
    )

    class Meta:
        model = ACINTPPolicy
        fields = (
            "aci_fabric",
            "aci_tenant",
            "name",
            "name_alias",
            "admin_state",
            "server_state_default",
            "auth_state",
            "description",
            "tags",
        )


# ===========================================================================
# NTP Provider
# ===========================================================================


class ACINTPProviderForm(NetBoxModelForm):
    ntp_policy = DynamicModelChoiceField(queryset=ACINTPPolicy.objects.all(), label=_("NTP Policy"))

    class Meta:
        model = ACINTPProvider
        fields = (
            "ntp_policy",
            "host",
            "name",
            "name_alias",
            "role",
            "min_poll",
            "max_poll",
            "key_id",
            "mgmt_epg",
            "description",
            "tags",
        )


class ACINTPProviderBulkEditForm(NetBoxModelBulkEditForm):
    model = ACINTPProvider
    role = forms.ChoiceField(choices=NTPProviderStateChoices, required=False)
    mgmt_epg = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "mgmt_epg", "key_id")


class ACINTPProviderFilterForm(NetBoxModelFilterSetForm):
    model = ACINTPProvider
    ntp_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACINTPPolicy.objects.all(), required=False, label=_("NTP Policy")
    )
    role = forms.MultipleChoiceField(choices=NTPProviderStateChoices, required=False)


class ACINTPProviderImportForm(NetBoxModelImportForm):
    ntp_policy = forms.ModelChoiceField(queryset=ACINTPPolicy.objects.all(), to_field_name="name")

    class Meta:
        model = ACINTPProvider
        fields = (
            "ntp_policy",
            "host",
            "name",
            "name_alias",
            "role",
            "min_poll",
            "max_poll",
            "key_id",
            "mgmt_epg",
            "description",
            "tags",
        )


# ===========================================================================
# Syslog Policy
# ===========================================================================


class ACISyslogPolicyForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    aci_tenant = DynamicModelChoiceField(
        queryset=ACITenant.objects.all(),
        required=False,
        label=_("Tenant"),
        query_params={"aci_fabric_id": "$aci_fabric"},
    )

    class Meta:
        model = ACISyslogPolicy
        fields = (
            "aci_fabric",
            "aci_tenant",
            "name",
            "name_alias",
            "admin_state",
            "console_severity",
            "local_severity",
            "include_msec",
            "include_tz",
            "description",
            "tags",
        )


class ACISyslogPolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISyslogPolicy
    admin_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    console_severity = forms.ChoiceField(choices=SyslogSeverityChoices, required=False)
    local_severity = forms.ChoiceField(choices=SyslogSeverityChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "aci_tenant")


class ACISyslogPolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACISyslogPolicy
    aci_fabric_id = _fabric_filter_field()
    aci_tenant_id = _tenant_filter_field()
    admin_state = forms.MultipleChoiceField(choices=EnabledDisabledChoices, required=False)
    console_severity = forms.MultipleChoiceField(choices=SyslogSeverityChoices, required=False)
    local_severity = forms.MultipleChoiceField(choices=SyslogSeverityChoices, required=False)


class ACISyslogPolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")
    aci_tenant = forms.ModelChoiceField(
        queryset=ACITenant.objects.all(), to_field_name="name", required=False
    )

    class Meta:
        model = ACISyslogPolicy
        fields = (
            "aci_fabric",
            "aci_tenant",
            "name",
            "name_alias",
            "admin_state",
            "console_severity",
            "local_severity",
            "include_msec",
            "include_tz",
            "description",
            "tags",
        )


# ===========================================================================
# Syslog Remote Destination
# ===========================================================================


class ACISyslogRemoteDestForm(NetBoxModelForm):
    syslog_policy = DynamicModelChoiceField(
        queryset=ACISyslogPolicy.objects.all(), label=_("Syslog Policy")
    )

    class Meta:
        model = ACISyslogRemoteDest
        fields = (
            "syslog_policy",
            "host",
            "port",
            "name",
            "name_alias",
            "severity",
            "forwarding_facility",
            "admin_state",
            "mgmt_epg",
            "description",
            "tags",
        )


class ACISyslogRemoteDestBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISyslogRemoteDest
    severity = forms.ChoiceField(choices=SyslogSeverityChoices, required=False)
    forwarding_facility = forms.ChoiceField(choices=SyslogFacilityChoices, required=False)
    admin_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "mgmt_epg")


class ACISyslogRemoteDestFilterForm(NetBoxModelFilterSetForm):
    model = ACISyslogRemoteDest
    syslog_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACISyslogPolicy.objects.all(), required=False, label=_("Syslog Policy")
    )
    severity = forms.MultipleChoiceField(choices=SyslogSeverityChoices, required=False)
    forwarding_facility = forms.MultipleChoiceField(choices=SyslogFacilityChoices, required=False)


class ACISyslogRemoteDestImportForm(NetBoxModelImportForm):
    syslog_policy = forms.ModelChoiceField(
        queryset=ACISyslogPolicy.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACISyslogRemoteDest
        fields = (
            "syslog_policy",
            "host",
            "port",
            "name",
            "name_alias",
            "severity",
            "forwarding_facility",
            "admin_state",
            "mgmt_epg",
            "description",
            "tags",
        )


# ===========================================================================
# SNMP Policy
# ===========================================================================


class ACISNMPPolicyForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    aci_tenant = DynamicModelChoiceField(
        queryset=ACITenant.objects.all(),
        required=False,
        label=_("Tenant"),
        query_params={"aci_fabric_id": "$aci_fabric"},
    )

    class Meta:
        model = ACISNMPPolicy
        fields = (
            "aci_fabric",
            "aci_tenant",
            "name",
            "name_alias",
            "admin_state",
            "contact",
            "location",
            "description",
            "tags",
        )


class ACISNMPPolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISNMPPolicy
    admin_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    contact = forms.CharField(max_length=255, required=False)
    location = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "aci_tenant", "contact", "location")


class ACISNMPPolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACISNMPPolicy
    aci_fabric_id = _fabric_filter_field()
    aci_tenant_id = _tenant_filter_field()
    admin_state = forms.MultipleChoiceField(choices=EnabledDisabledChoices, required=False)


class ACISNMPPolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")
    aci_tenant = forms.ModelChoiceField(
        queryset=ACITenant.objects.all(), to_field_name="name", required=False
    )

    class Meta:
        model = ACISNMPPolicy
        fields = (
            "aci_fabric",
            "aci_tenant",
            "name",
            "name_alias",
            "admin_state",
            "contact",
            "location",
            "description",
            "tags",
        )


# ===========================================================================
# SNMP Community
# ===========================================================================


class ACISNMPCommunityForm(NetBoxModelForm):
    snmp_policy = DynamicModelChoiceField(
        queryset=ACISNMPPolicy.objects.all(), label=_("SNMP Policy")
    )

    class Meta:
        model = ACISNMPCommunity
        fields = ("snmp_policy", "name", "name_alias", "description", "tags")


class ACISNMPCommunityBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISNMPCommunity
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACISNMPCommunityFilterForm(NetBoxModelFilterSetForm):
    model = ACISNMPCommunity
    snmp_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACISNMPPolicy.objects.all(), required=False, label=_("SNMP Policy")
    )


class ACISNMPCommunityImportForm(NetBoxModelImportForm):
    snmp_policy = forms.ModelChoiceField(queryset=ACISNMPPolicy.objects.all(), to_field_name="name")

    class Meta:
        model = ACISNMPCommunity
        fields = ("snmp_policy", "name", "name_alias", "description", "tags")


# ===========================================================================
# SNMP Client Group
# ===========================================================================


class ACISNMPClientGroupForm(NetBoxModelForm):
    snmp_policy = DynamicModelChoiceField(
        queryset=ACISNMPPolicy.objects.all(), label=_("SNMP Policy")
    )

    class Meta:
        model = ACISNMPClientGroup
        fields = ("snmp_policy", "name", "name_alias", "mgmt_epg", "description", "tags")


class ACISNMPClientGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISNMPClientGroup
    mgmt_epg = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "mgmt_epg")


class ACISNMPClientGroupFilterForm(NetBoxModelFilterSetForm):
    model = ACISNMPClientGroup
    snmp_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACISNMPPolicy.objects.all(), required=False, label=_("SNMP Policy")
    )


class ACISNMPClientGroupImportForm(NetBoxModelImportForm):
    snmp_policy = forms.ModelChoiceField(queryset=ACISNMPPolicy.objects.all(), to_field_name="name")

    class Meta:
        model = ACISNMPClientGroup
        fields = ("snmp_policy", "name", "name_alias", "mgmt_epg", "description", "tags")


# ===========================================================================
# SNMP Client
# ===========================================================================


class ACISNMPClientForm(NetBoxModelForm):
    client_group = DynamicModelChoiceField(
        queryset=ACISNMPClientGroup.objects.all(), label=_("Client Group")
    )

    class Meta:
        model = ACISNMPClient
        fields = ("client_group", "name", "address", "description", "tags")


class ACISNMPClientBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISNMPClient
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACISNMPClientFilterForm(NetBoxModelFilterSetForm):
    model = ACISNMPClient
    client_group_id = DynamicModelMultipleChoiceField(
        queryset=ACISNMPClientGroup.objects.all(), required=False, label=_("Client Group")
    )


class ACISNMPClientImportForm(NetBoxModelImportForm):
    client_group = forms.ModelChoiceField(
        queryset=ACISNMPClientGroup.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACISNMPClient
        fields = ("client_group", "name", "address", "description", "tags")


# ===========================================================================
# SNMP v3 User
# ===========================================================================


class ACISNMPv3UserForm(NetBoxModelForm):
    snmp_policy = DynamicModelChoiceField(
        queryset=ACISNMPPolicy.objects.all(), label=_("SNMP Policy")
    )

    class Meta:
        model = ACISNMPv3User
        fields = (
            "snmp_policy",
            "name",
            "name_alias",
            "auth_protocol",
            "privacy_protocol",
            "description",
            "tags",
        )


class ACISNMPv3UserBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISNMPv3User
    auth_protocol = forms.ChoiceField(choices=SNMPAuthProtocolChoices, required=False)
    privacy_protocol = forms.ChoiceField(choices=SNMPPrivProtocolChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACISNMPv3UserFilterForm(NetBoxModelFilterSetForm):
    model = ACISNMPv3User
    snmp_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACISNMPPolicy.objects.all(), required=False, label=_("SNMP Policy")
    )
    auth_protocol = forms.MultipleChoiceField(choices=SNMPAuthProtocolChoices, required=False)
    privacy_protocol = forms.MultipleChoiceField(choices=SNMPPrivProtocolChoices, required=False)


class ACISNMPv3UserImportForm(NetBoxModelImportForm):
    snmp_policy = forms.ModelChoiceField(queryset=ACISNMPPolicy.objects.all(), to_field_name="name")

    class Meta:
        model = ACISNMPv3User
        fields = (
            "snmp_policy",
            "name",
            "name_alias",
            "auth_protocol",
            "privacy_protocol",
            "description",
            "tags",
        )


# ===========================================================================
# SNMP Trap Policy
# ===========================================================================


class ACISNMPTrapPolicyForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    aci_tenant = DynamicModelChoiceField(
        queryset=ACITenant.objects.all(),
        required=False,
        label=_("Tenant"),
        query_params={"aci_fabric_id": "$aci_fabric"},
    )

    class Meta:
        model = ACISNMPTrapPolicy
        fields = (
            "aci_fabric",
            "aci_tenant",
            "name",
            "name_alias",
            "admin_state",
            "description",
            "tags",
        )


class ACISNMPTrapPolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISNMPTrapPolicy
    admin_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "aci_tenant")


class ACISNMPTrapPolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACISNMPTrapPolicy
    aci_fabric_id = _fabric_filter_field()
    aci_tenant_id = _tenant_filter_field()
    admin_state = forms.MultipleChoiceField(choices=EnabledDisabledChoices, required=False)


class ACISNMPTrapPolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")
    aci_tenant = forms.ModelChoiceField(
        queryset=ACITenant.objects.all(), to_field_name="name", required=False
    )

    class Meta:
        model = ACISNMPTrapPolicy
        fields = (
            "aci_fabric",
            "aci_tenant",
            "name",
            "name_alias",
            "admin_state",
            "description",
            "tags",
        )


# ===========================================================================
# SNMP Trap Destination
# ===========================================================================


class ACISNMPTrapDestForm(NetBoxModelForm):
    trap_policy = DynamicModelChoiceField(
        queryset=ACISNMPTrapPolicy.objects.all(), label=_("SNMP Trap Policy")
    )

    class Meta:
        model = ACISNMPTrapDest
        fields = (
            "trap_policy",
            "host",
            "port",
            "name",
            "name_alias",
            "version",
            "community_or_user",
            "v3_security_level",
            "mgmt_epg",
            "description",
            "tags",
        )


class ACISNMPTrapDestBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISNMPTrapDest
    version = forms.ChoiceField(choices=SNMPVersionChoices, required=False)
    v3_security_level = forms.ChoiceField(choices=SNMPSecurityLevelChoices, required=False)
    mgmt_epg = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "v3_security_level", "mgmt_epg")


class ACISNMPTrapDestFilterForm(NetBoxModelFilterSetForm):
    model = ACISNMPTrapDest
    trap_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACISNMPTrapPolicy.objects.all(), required=False, label=_("SNMP Trap Policy")
    )
    version = forms.MultipleChoiceField(choices=SNMPVersionChoices, required=False)


class ACISNMPTrapDestImportForm(NetBoxModelImportForm):
    trap_policy = forms.ModelChoiceField(
        queryset=ACISNMPTrapPolicy.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACISNMPTrapDest
        fields = (
            "trap_policy",
            "host",
            "port",
            "name",
            "name_alias",
            "version",
            "community_or_user",
            "v3_security_level",
            "mgmt_epg",
            "description",
            "tags",
        )


# ===========================================================================
# Pod Policy Group
# ===========================================================================


class ACIPodPolicyGroupForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    ntp_policy = DynamicModelChoiceField(
        queryset=ACINTPPolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    syslog_policy = DynamicModelChoiceField(
        queryset=ACISyslogPolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    snmp_policy = DynamicModelChoiceField(
        queryset=ACISNMPPolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    snmp_trap_policy = DynamicModelChoiceField(
        queryset=ACISNMPTrapPolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )

    class Meta:
        model = ACIPodPolicyGroup
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "ntp_policy",
            "syslog_policy",
            "snmp_policy",
            "snmp_trap_policy",
            "description",
            "tags",
        )


class ACIPodPolicyGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIPodPolicyGroup
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    ntp_policy = DynamicModelChoiceField(queryset=ACINTPPolicy.objects.all(), required=False)
    syslog_policy = DynamicModelChoiceField(queryset=ACISyslogPolicy.objects.all(), required=False)
    snmp_policy = DynamicModelChoiceField(queryset=ACISNMPPolicy.objects.all(), required=False)
    snmp_trap_policy = DynamicModelChoiceField(
        queryset=ACISNMPTrapPolicy.objects.all(), required=False
    )
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = (
        "description",
        "name_alias",
        "ntp_policy",
        "syslog_policy",
        "snmp_policy",
        "snmp_trap_policy",
    )


class ACIPodPolicyGroupFilterForm(NetBoxModelFilterSetForm):
    model = ACIPodPolicyGroup
    aci_fabric_id = _fabric_filter_field()
    ntp_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACINTPPolicy.objects.all(), required=False, label=_("NTP Policy")
    )
    syslog_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACISyslogPolicy.objects.all(), required=False, label=_("Syslog Policy")
    )
    snmp_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACISNMPPolicy.objects.all(), required=False, label=_("SNMP Policy")
    )
    snmp_trap_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACISNMPTrapPolicy.objects.all(), required=False, label=_("SNMP Trap Policy")
    )


class ACIPodPolicyGroupImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")
    ntp_policy = forms.ModelChoiceField(
        queryset=ACINTPPolicy.objects.all(), to_field_name="name", required=False
    )
    syslog_policy = forms.ModelChoiceField(
        queryset=ACISyslogPolicy.objects.all(), to_field_name="name", required=False
    )
    snmp_policy = forms.ModelChoiceField(
        queryset=ACISNMPPolicy.objects.all(), to_field_name="name", required=False
    )
    snmp_trap_policy = forms.ModelChoiceField(
        queryset=ACISNMPTrapPolicy.objects.all(), to_field_name="name", required=False
    )

    class Meta:
        model = ACIPodPolicyGroup
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "ntp_policy",
            "syslog_policy",
            "snmp_policy",
            "snmp_trap_policy",
            "description",
            "tags",
        )
