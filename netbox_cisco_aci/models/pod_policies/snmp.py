"""ACI SNMP policy, communities, client groups, clients, and v3 users.

Maps to APIC's ``snmpPol``, ``snmpCommunityP``, ``snmpClientGrpP``,
``snmpClientP``, and ``snmpUserP``.
"""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import SNMPAuthProtocolChoices, SNMPPrivProtocolChoices
from ..base import ACIBaseModel
from ._base import _PodPolicyBase


class ACISNMPPolicy(_PodPolicyBase):
    """SNMP policy that contains communities, v3 users, and client groups."""

    contact = models.CharField(
        verbose_name=_("sysContact"),
        max_length=255,
        blank=True,
        help_text=_("RFC 1213 sysContact MIB-II OID value."),
    )
    location = models.CharField(
        verbose_name=_("sysLocation"),
        max_length=255,
        blank=True,
        help_text=_("RFC 1213 sysLocation MIB-II OID value."),
    )

    clone_fields = (
        "aci_fabric",
        "aci_tenant",
        "admin_state",
        "contact",
        "location",
        "description",
    )

    class Meta(_PodPolicyBase.Meta):
        verbose_name = _("ACI SNMP Policy")
        verbose_name_plural = _("ACI SNMP Policies")
        # See ACINTPPolicy.Meta for why uniqueness is split across two
        # partial constraints on the nullable ``aci_tenant`` column.
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                condition=models.Q(aci_tenant__isnull=True),
                name="netbox_cisco_aci_acisnmp_fabric_name_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_fabric", "aci_tenant", "name"),
                condition=models.Q(aci_tenant__isnull=False),
                name="netbox_cisco_aci_acisnmp_fabric_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        scope = self.aci_tenant.name if self.aci_tenant_id else "fabric"
        return f"{self.aci_fabric.name} / {scope} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisnmppolicy", args=[self.pk])


class ACISNMPCommunity(ACIBaseModel):
    """SNMP v1/v2c community string.

    We store the community *name* in the standard ``name`` column so the
    rest of the plugin's name handling just works; the actual community
    secret is not stored here.
    """

    snmp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISNMPPolicy",
        on_delete=models.CASCADE,
        related_name="communities",
        verbose_name=_("SNMP Policy"),
    )

    clone_fields = ("snmp_policy", "description")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI SNMP Community")
        verbose_name_plural = _("ACI SNMP Communities")
        constraints = (
            models.UniqueConstraint(
                fields=("snmp_policy", "name"),
                name="netbox_cisco_aci_acisnmpcomm_policy_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.snmp_policy.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisnmpcommunity", args=[self.pk])


class ACISNMPClientGroup(ACIBaseModel):
    """SNMP client group: an ACL-like set of client IPs/CIDRs that may query a policy."""

    snmp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISNMPPolicy",
        on_delete=models.CASCADE,
        related_name="client_groups",
        verbose_name=_("SNMP Policy"),
    )
    mgmt_epg = models.CharField(
        verbose_name=_("Management EPG"),
        max_length=255,
        blank=True,
    )

    clone_fields = ("snmp_policy", "mgmt_epg", "description")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI SNMP Client Group")
        verbose_name_plural = _("ACI SNMP Client Groups")
        constraints = (
            models.UniqueConstraint(
                fields=("snmp_policy", "name"),
                name="netbox_cisco_aci_acisnmpclientgrp_policy_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.snmp_policy.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisnmpclientgroup", args=[self.pk])


class ACISNMPClient(ACIBaseModel):
    """One client IP/CIDR inside an SNMP client group."""

    client_group = models.ForeignKey(
        to="netbox_cisco_aci.ACISNMPClientGroup",
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name=_("Client Group"),
    )
    address = models.CharField(
        verbose_name=_("Address"),
        max_length=64,
        help_text=_("Single IP or CIDR (e.g. 10.0.0.0/24)."),
    )

    clone_fields = ("client_group", "address")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI SNMP Client")
        verbose_name_plural = _("ACI SNMP Clients")
        constraints = (
            models.UniqueConstraint(
                fields=("client_group", "address"),
                name="netbox_cisco_aci_acisnmpclient_grp_address_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.client_group.name} / {self.address}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisnmpclient", args=[self.pk])


class ACISNMPv3User(ACIBaseModel):
    """SNMPv3 user record (operational reference only — secrets live on APIC)."""

    snmp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISNMPPolicy",
        on_delete=models.CASCADE,
        related_name="v3_users",
        verbose_name=_("SNMP Policy"),
    )
    auth_protocol = models.CharField(
        verbose_name=_("Auth protocol"),
        max_length=32,
        choices=SNMPAuthProtocolChoices,
        default=SNMPAuthProtocolChoices.SHA,
    )
    privacy_protocol = models.CharField(
        verbose_name=_("Privacy protocol"),
        max_length=16,
        choices=SNMPPrivProtocolChoices,
        default=SNMPPrivProtocolChoices.AES128,
    )

    clone_fields = ("snmp_policy", "auth_protocol", "privacy_protocol", "description")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI SNMP v3 User")
        verbose_name_plural = _("ACI SNMP v3 Users")
        constraints = (
            models.UniqueConstraint(
                fields=("snmp_policy", "name"),
                name="netbox_cisco_aci_acisnmpv3_policy_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.snmp_policy.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisnmpv3user", args=[self.pk])
