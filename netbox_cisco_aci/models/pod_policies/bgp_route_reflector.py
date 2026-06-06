"""ACI BGP Route Reflector policy + its spine-node list.

Maps APIC's ``bgpRRP`` / ``bgpRRNodePEp`` MOs. The parent declares the
fabric-overlay AS number; the children pin which spine ``node_id``s
act as route reflectors for that AS.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...constants import NODE_ID_MAX, NODE_ID_MIN
from ..base import ACIBaseModel
from ._base import _PodPolicyBase


class ACIBGPRouteReflectorPolicy(_PodPolicyBase):
    """BGP route reflector policy for the fabric overlay (``bgpRRP``)."""

    autonomous_system_number = models.PositiveBigIntegerField(
        verbose_name=_("Autonomous system number"),
        validators=[MinValueValidator(1), MaxValueValidator(4_294_967_295)],
        help_text=_(
            "32-bit ASN used by the fabric overlay BGP route reflectors. "
            "Common values are 65000\u201365534 for private ASNs."
        ),
    )

    clone_fields = (
        "aci_fabric",
        "aci_tenant",
        "admin_state",
        "autonomous_system_number",
        "description",
    )

    class Meta(_PodPolicyBase.Meta):
        verbose_name = _("ACI BGP Route Reflector Policy")
        verbose_name_plural = _("ACI BGP Route Reflector Policies")
        # See ACINTPPolicy.Meta for why uniqueness is split across two
        # partial constraints on the nullable ``aci_tenant`` column.
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                condition=models.Q(aci_tenant__isnull=True),
                name="netbox_cisco_aci_acibgprr_fabric_name_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_fabric", "aci_tenant", "name"),
                condition=models.Q(aci_tenant__isnull=False),
                name="netbox_cisco_aci_acibgprr_fabric_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        scope = self.aci_tenant.name if self.aci_tenant_id else "fabric"
        return f"{self.aci_fabric.name} / {scope} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acibgproutereflectorpolicy", args=[self.pk])


class ACIBGPRouteReflectorNode(ACIBaseModel):
    """One spine node entry inside a BGP RR policy (``bgpRRNodePEp``).

    We store ``node_id`` as a plain integer rather than a FK to
    ``ACINode`` because (a) APIC accepts a node ID before the matching
    node exists, and (b) we don't want deleting a node row to silently
    strip its RR designation. Validation can be layered later.
    """

    bgp_rr_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACIBGPRouteReflectorPolicy",
        on_delete=models.CASCADE,
        related_name="rr_nodes",
        verbose_name=_("BGP RR Policy"),
    )
    node_id = models.PositiveIntegerField(
        verbose_name=_("Node ID"),
        validators=[MinValueValidator(NODE_ID_MIN), MaxValueValidator(NODE_ID_MAX)],
        help_text=_("APIC spine node ID that should act as a BGP route reflector."),
    )

    clone_fields = ("bgp_rr_policy", "description")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI BGP RR Node")
        verbose_name_plural = _("ACI BGP RR Nodes")
        constraints = (
            models.UniqueConstraint(
                fields=("bgp_rr_policy", "node_id"),
                name="netbox_cisco_aci_acibgprrnode_policy_nodeid_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.bgp_rr_policy.name} / node {self.node_id}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acibgproutereflectornode", args=[self.pk])
