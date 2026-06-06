"""DRF serializers for the pod-policy family."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.pod_policies import (
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
from .fabric import ACIFabricSerializer
from .tenant import ACITenantSerializer


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


# ---------------------------------------------------------------------------
# NTP
# ---------------------------------------------------------------------------


class ACINTPPolicySerializer(NetBoxModelSerializer):
    url = _url("acintppolicy")
    aci_fabric = ACIFabricSerializer(nested=True)
    aci_tenant = ACITenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACINTPPolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "server_state_default",
            "auth_state",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "aci_tenant",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


class ACINTPProviderSerializer(NetBoxModelSerializer):
    url = _url("acintpprovider")
    ntp_policy = ACINTPPolicySerializer(nested=True)

    class Meta:
        model = ACINTPProvider
        fields = (
            "id",
            "url",
            "display",
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
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "display",
            "host",
            "id",
            "name",
            "ntp_policy",
            "role",
            "url",
        )


# ---------------------------------------------------------------------------
# Syslog
# ---------------------------------------------------------------------------


class ACISyslogPolicySerializer(NetBoxModelSerializer):
    url = _url("acisyslogpolicy")
    aci_fabric = ACIFabricSerializer(nested=True)
    aci_tenant = ACITenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACISyslogPolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "console_severity",
            "local_severity",
            "include_msec",
            "include_tz",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "aci_tenant",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


class ACISyslogRemoteDestSerializer(NetBoxModelSerializer):
    url = _url("acisyslogremotedest")
    syslog_policy = ACISyslogPolicySerializer(nested=True)

    class Meta:
        model = ACISyslogRemoteDest
        fields = (
            "id",
            "url",
            "display",
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
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "display",
            "host",
            "id",
            "name",
            "port",
            "severity",
            "syslog_policy",
            "url",
        )


# ---------------------------------------------------------------------------
# SNMP
# ---------------------------------------------------------------------------


class ACISNMPPolicySerializer(NetBoxModelSerializer):
    url = _url("acisnmppolicy")
    aci_fabric = ACIFabricSerializer(nested=True)
    aci_tenant = ACITenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACISNMPPolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "contact",
            "location",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "aci_tenant",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


class ACISNMPCommunitySerializer(NetBoxModelSerializer):
    url = _url("acisnmpcommunity")
    snmp_policy = ACISNMPPolicySerializer(nested=True)

    class Meta:
        model = ACISNMPCommunity
        fields = (
            "id",
            "url",
            "display",
            "snmp_policy",
            "name",
            "name_alias",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("display", "id", "name", "snmp_policy", "url")


class ACISNMPClientGroupSerializer(NetBoxModelSerializer):
    url = _url("acisnmpclientgroup")
    snmp_policy = ACISNMPPolicySerializer(nested=True)

    class Meta:
        model = ACISNMPClientGroup
        fields = (
            "id",
            "url",
            "display",
            "snmp_policy",
            "name",
            "name_alias",
            "mgmt_epg",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("display", "id", "mgmt_epg", "name", "snmp_policy", "url")


class ACISNMPClientSerializer(NetBoxModelSerializer):
    url = _url("acisnmpclient")
    client_group = ACISNMPClientGroupSerializer(nested=True)

    class Meta:
        model = ACISNMPClient
        fields = (
            "id",
            "url",
            "display",
            "client_group",
            "name",
            "address",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("address", "client_group", "display", "id", "name", "url")


class ACISNMPv3UserSerializer(NetBoxModelSerializer):
    url = _url("acisnmpv3user")
    snmp_policy = ACISNMPPolicySerializer(nested=True)

    class Meta:
        model = ACISNMPv3User
        fields = (
            "id",
            "url",
            "display",
            "snmp_policy",
            "name",
            "name_alias",
            "auth_protocol",
            "privacy_protocol",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "auth_protocol",
            "display",
            "id",
            "name",
            "privacy_protocol",
            "snmp_policy",
            "url",
        )


# ---------------------------------------------------------------------------
# SNMP Traps
# ---------------------------------------------------------------------------


class ACISNMPTrapPolicySerializer(NetBoxModelSerializer):
    url = _url("acisnmptrappolicy")
    aci_fabric = ACIFabricSerializer(nested=True)
    aci_tenant = ACITenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACISNMPTrapPolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "aci_tenant",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


class ACISNMPTrapDestSerializer(NetBoxModelSerializer):
    url = _url("acisnmptrapdest")
    trap_policy = ACISNMPTrapPolicySerializer(nested=True)

    class Meta:
        model = ACISNMPTrapDest
        fields = (
            "id",
            "url",
            "display",
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
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "display",
            "host",
            "id",
            "name",
            "port",
            "trap_policy",
            "url",
            "version",
        )


# ---------------------------------------------------------------------------
# Pod Policy Group
# ---------------------------------------------------------------------------


class ACIPodPolicyGroupSerializer(NetBoxModelSerializer):
    url = _url("acipodpolicygroup")
    aci_fabric = ACIFabricSerializer(nested=True)
    ntp_policy = ACINTPPolicySerializer(nested=True, required=False, allow_null=True)
    syslog_policy = ACISyslogPolicySerializer(nested=True, required=False, allow_null=True)
    snmp_policy = ACISNMPPolicySerializer(nested=True, required=False, allow_null=True)
    snmp_trap_policy = ACISNMPTrapPolicySerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACIPodPolicyGroup
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "ntp_policy",
            "syslog_policy",
            "snmp_policy",
            "snmp_trap_policy",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "description",
            "display",
            "id",
            "name",
            "url",
        )
