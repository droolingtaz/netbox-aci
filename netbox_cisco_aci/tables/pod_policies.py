"""Tables for the pod-policy family (NTP / Syslog / SNMP / SNMP Traps)."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

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


def _tag_col(list_url: str) -> columns.TagColumn:
    return columns.TagColumn(url_name=f"plugins:netbox_cisco_aci:{list_url}_list")


# ---------------------------------------------------------------------------
# NTP
# ---------------------------------------------------------------------------


class ACINTPPolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    admin_state = ChoiceFieldColumn()
    server_state_default = ChoiceFieldColumn(verbose_name="Default role")
    tags = _tag_col("acintppolicy")

    class Meta(NetBoxTable.Meta):
        model = ACINTPPolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "server_state_default",
            "auth_state",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "server_state_default",
        )


class ACINTPProviderTable(NetBoxTable):
    host = tables.Column(linkify=True)
    ntp_policy = tables.Column(linkify=True, verbose_name="NTP Policy")
    role = ChoiceFieldColumn()
    tags = _tag_col("acintpprovider")

    class Meta(NetBoxTable.Meta):
        model = ACINTPProvider
        fields = (
            "pk",
            "id",
            "host",
            "ntp_policy",
            "name",
            "role",
            "min_poll",
            "max_poll",
            "key_id",
            "mgmt_epg",
            "description",
            "tags",
        )
        default_columns = ("host", "ntp_policy", "role", "min_poll", "max_poll")


# ---------------------------------------------------------------------------
# Syslog
# ---------------------------------------------------------------------------


class ACISyslogPolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    admin_state = ChoiceFieldColumn()
    console_severity = ChoiceFieldColumn(verbose_name="Console")
    local_severity = ChoiceFieldColumn(verbose_name="Local")
    tags = _tag_col("acisyslogpolicy")

    class Meta(NetBoxTable.Meta):
        model = ACISyslogPolicy
        fields = (
            "pk",
            "id",
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
        )
        default_columns = (
            "name",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "console_severity",
            "local_severity",
        )


class ACISyslogRemoteDestTable(NetBoxTable):
    host = tables.Column(linkify=True)
    syslog_policy = tables.Column(linkify=True, verbose_name="Syslog Policy")
    severity = ChoiceFieldColumn()
    forwarding_facility = ChoiceFieldColumn(verbose_name="Facility")
    admin_state = ChoiceFieldColumn()
    tags = _tag_col("acisyslogremotedest")

    class Meta(NetBoxTable.Meta):
        model = ACISyslogRemoteDest
        fields = (
            "pk",
            "id",
            "host",
            "port",
            "syslog_policy",
            "name",
            "severity",
            "forwarding_facility",
            "admin_state",
            "mgmt_epg",
            "description",
            "tags",
        )
        default_columns = (
            "host",
            "port",
            "syslog_policy",
            "severity",
            "forwarding_facility",
            "admin_state",
        )


# ---------------------------------------------------------------------------
# SNMP
# ---------------------------------------------------------------------------


class ACISNMPPolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    admin_state = ChoiceFieldColumn()
    tags = _tag_col("acisnmppolicy")

    class Meta(NetBoxTable.Meta):
        model = ACISNMPPolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "contact",
            "location",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "aci_tenant", "admin_state", "contact")


class ACISNMPCommunityTable(NetBoxTable):
    name = tables.Column(linkify=True, verbose_name="Community")
    snmp_policy = tables.Column(linkify=True, verbose_name="SNMP Policy")
    tags = _tag_col("acisnmpcommunity")

    class Meta(NetBoxTable.Meta):
        model = ACISNMPCommunity
        fields = ("pk", "id", "name", "snmp_policy", "description", "tags")
        default_columns = ("name", "snmp_policy", "description")


class ACISNMPClientGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    snmp_policy = tables.Column(linkify=True, verbose_name="SNMP Policy")
    tags = _tag_col("acisnmpclientgroup")

    class Meta(NetBoxTable.Meta):
        model = ACISNMPClientGroup
        fields = ("pk", "id", "name", "snmp_policy", "mgmt_epg", "description", "tags")
        default_columns = ("name", "snmp_policy", "mgmt_epg")


class ACISNMPClientTable(NetBoxTable):
    address = tables.Column(linkify=True)
    client_group = tables.Column(linkify=True, verbose_name="Client Group")
    tags = _tag_col("acisnmpclient")

    class Meta(NetBoxTable.Meta):
        model = ACISNMPClient
        fields = ("pk", "id", "address", "client_group", "name", "description", "tags")
        default_columns = ("address", "client_group", "name")


class ACISNMPv3UserTable(NetBoxTable):
    name = tables.Column(linkify=True)
    snmp_policy = tables.Column(linkify=True, verbose_name="SNMP Policy")
    auth_protocol = ChoiceFieldColumn(verbose_name="Auth")
    privacy_protocol = ChoiceFieldColumn(verbose_name="Privacy")
    tags = _tag_col("acisnmpv3user")

    class Meta(NetBoxTable.Meta):
        model = ACISNMPv3User
        fields = (
            "pk",
            "id",
            "name",
            "snmp_policy",
            "auth_protocol",
            "privacy_protocol",
            "description",
            "tags",
        )
        default_columns = ("name", "snmp_policy", "auth_protocol", "privacy_protocol")


# ---------------------------------------------------------------------------
# SNMP Traps
# ---------------------------------------------------------------------------


class ACISNMPTrapPolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    admin_state = ChoiceFieldColumn()
    tags = _tag_col("acisnmptrappolicy")

    class Meta(NetBoxTable.Meta):
        model = ACISNMPTrapPolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "aci_tenant",
            "admin_state",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "aci_tenant", "admin_state")


class ACISNMPTrapDestTable(NetBoxTable):
    host = tables.Column(linkify=True)
    trap_policy = tables.Column(linkify=True, verbose_name="Trap Policy")
    version = ChoiceFieldColumn()
    v3_security_level = ChoiceFieldColumn(verbose_name="v3 sec level")
    tags = _tag_col("acisnmptrapdest")

    class Meta(NetBoxTable.Meta):
        model = ACISNMPTrapDest
        fields = (
            "pk",
            "id",
            "host",
            "port",
            "trap_policy",
            "name",
            "version",
            "community_or_user",
            "v3_security_level",
            "mgmt_epg",
            "description",
            "tags",
        )
        default_columns = (
            "host",
            "port",
            "trap_policy",
            "version",
            "community_or_user",
        )


# ---------------------------------------------------------------------------
# Pod Policy Group
# ---------------------------------------------------------------------------


class ACIPodPolicyGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    ntp_policy = tables.Column(linkify=True, verbose_name="NTP")
    syslog_policy = tables.Column(linkify=True, verbose_name="Syslog")
    snmp_policy = tables.Column(linkify=True, verbose_name="SNMP")
    snmp_trap_policy = tables.Column(linkify=True, verbose_name="SNMP Trap")
    tags = _tag_col("acipodpolicygroup")

    class Meta(NetBoxTable.Meta):
        model = ACIPodPolicyGroup
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "ntp_policy",
            "syslog_policy",
            "snmp_policy",
            "snmp_trap_policy",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_fabric",
            "ntp_policy",
            "syslog_policy",
            "snmp_policy",
            "snmp_trap_policy",
        )
