"""ACI COOP (Council of Oracles Protocol) group policy.

Maps APIC's ``coopPol``. The single configurable knob is the
authentication mode between spines that share the COOP database
(``strict`` for MD5 auth required, ``compatible`` for legacy fabrics).
"""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import COOPAuthenticationTypeChoices
from ._base import _PodPolicyBase


class ACICOOPGroupPolicy(_PodPolicyBase):
    """COOP authentication policy applied to spine \u2194 spine endpoint sync."""

    authentication_type = models.CharField(
        verbose_name=_("Authentication type"),
        max_length=16,
        choices=COOPAuthenticationTypeChoices,
        default=COOPAuthenticationTypeChoices.STRICT,
        help_text=_(
            "``strict`` enforces MD5 authentication between spines (modern "
            "default). ``compatible`` accepts unauthenticated peers; only "
            "use it during migration windows."
        ),
    )

    clone_fields = (
        "aci_fabric",
        "aci_tenant",
        "admin_state",
        "authentication_type",
        "description",
    )

    class Meta(_PodPolicyBase.Meta):
        verbose_name = _("ACI COOP Group Policy")
        verbose_name_plural = _("ACI COOP Group Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                condition=models.Q(aci_tenant__isnull=True),
                name="netbox_cisco_aci_acicoop_fabric_name_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_fabric", "aci_tenant", "name"),
                condition=models.Q(aci_tenant__isnull=False),
                name="netbox_cisco_aci_acicoop_fabric_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        scope = self.aci_tenant.name if self.aci_tenant_id else "fabric"
        return f"{self.aci_fabric.name} / {scope} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acicoopgrouppolicy", args=[self.pk])
