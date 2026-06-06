"""Internal helpers shared by every pod-policy model.

All four policy families (NTP, Syslog, SNMP, SNMP Traps) have the same
shape at the parent level: required FK to ACIFabric, optional FK to
ACITenant (for per-tenant overrides), the standard ACI name/alias/
description block from ``ACIBaseModel``, and an enabled/disabled admin
state. Factoring that out keeps each concrete model file focused on the
fields that actually differ.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from ...choices import EnabledDisabledChoices
from ..base import ACIBaseModel


class _PodPolicyBase(ACIBaseModel):
    """Fabric-scoped policy with optional per-tenant override.

    Subclasses must add their own ``Meta`` (with verbose_name /
    constraints / etc.) and any policy-specific fields. The shared
    Meta on this class is abstract and only sets ``ordering``.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("ACI Fabric"),
    )
    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("ACI Tenant"),
        null=True,
        blank=True,
        help_text=_(
            "Optional. Leave blank for a fabric-wide policy; set to scope "
            "this policy to a single tenant's monitoring overrides."
        ),
    )
    admin_state = models.CharField(
        verbose_name=_("Admin state"),
        max_length=16,
        choices=EnabledDisabledChoices,
        default=EnabledDisabledChoices.ENABLED,
    )

    class Meta(ACIBaseModel.Meta):
        abstract = True
