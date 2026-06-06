"""ACI SNMP Trap policy and trap forwarder destinations.

Maps to APIC's ``snmpTrapFwdServerP`` group under Monitoring Policies.
"""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import SNMPSecurityLevelChoices, SNMPVersionChoices
from ..base import ACIBaseModel
from ._base import _PodPolicyBase


class ACISNMPTrapPolicy(_PodPolicyBase):
    """Container for SNMP trap forwarder destinations.

    Each ACISNMPTrapPolicy belongs to a fabric (optionally to a tenant
    for per-tenant overrides) and groups one or more trap destinations
    that the fabric will forward SNMP traps to.
    """

    clone_fields = ("aci_fabric", "aci_tenant", "admin_state", "description")

    class Meta(_PodPolicyBase.Meta):
        verbose_name = _("ACI SNMP Trap Policy")
        verbose_name_plural = _("ACI SNMP Trap Policies")
        # See ACINTPPolicy.Meta for why uniqueness is split across two
        # partial constraints on the nullable ``aci_tenant`` column.
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                condition=models.Q(aci_tenant__isnull=True),
                name="netbox_cisco_aci_acisnmptrap_fabric_name_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_fabric", "aci_tenant", "name"),
                condition=models.Q(aci_tenant__isnull=False),
                name="netbox_cisco_aci_acisnmptrap_fabric_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        scope = self.aci_tenant.name if self.aci_tenant_id else "fabric"
        return f"{self.aci_fabric.name} / {scope} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisnmptrappolicy", args=[self.pk])


class ACISNMPTrapDest(ACIBaseModel):
    """One trap forwarder inside an SNMP Trap policy."""

    trap_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISNMPTrapPolicy",
        on_delete=models.CASCADE,
        related_name="destinations",
        verbose_name=_("SNMP Trap Policy"),
    )
    host = models.CharField(
        verbose_name=_("Host"),
        max_length=255,
        help_text=_("FQDN or IP of the trap collector."),
    )
    port = models.PositiveIntegerField(
        verbose_name=_("Port"),
        default=162,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    version = models.CharField(
        verbose_name=_("SNMP version"),
        max_length=8,
        choices=SNMPVersionChoices,
        default=SNMPVersionChoices.V2C,
    )
    # For v1/v2c this is the community string; for v3 this is the user name.
    # We keep one column rather than two so a single index can search
    # forwarders regardless of version.
    community_or_user = models.CharField(
        verbose_name=_("Community / User"),
        max_length=255,
        blank=True,
        help_text=_(
            "v1/v2c: the community string the trap will be sent with. "
            "v3: the SNMPv3 user name to use. Leave blank if APIC will "
            "resolve it via the policy's communities/users list."
        ),
    )
    v3_security_level = models.CharField(
        verbose_name=_("v3 security level"),
        max_length=16,
        choices=SNMPSecurityLevelChoices,
        blank=True,
        help_text=_("Only meaningful when version=v3. Ignored on v1/v2c traps."),
    )
    mgmt_epg = models.CharField(
        verbose_name=_("Management EPG"),
        max_length=255,
        blank=True,
    )

    clone_fields = (
        "trap_policy",
        "port",
        "version",
        "v3_security_level",
        "mgmt_epg",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI SNMP Trap Destination")
        verbose_name_plural = _("ACI SNMP Trap Destinations")
        constraints = (
            models.UniqueConstraint(
                fields=("trap_policy", "host", "port"),
                name="netbox_cisco_aci_acisnmptrapdest_policy_host_port_unique",
            ),
        )

    def clean(self) -> None:
        super().clean()
        # v3 security level is only meaningful for v3 traps; surface a
        # validation error rather than silently storing nonsense.
        if self.version != SNMPVersionChoices.V3 and self.v3_security_level:
            raise ValidationError(
                {"v3_security_level": _("v3 security level is only valid when version is v3.")}
            )

    def __str__(self) -> str:
        return f"{self.trap_policy.name} / {self.host}:{self.port}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisnmptrapdest", args=[self.pk])
