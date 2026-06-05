"""ACI BFD Interface Policy + Attachment (``bfdIfPol`` / ``bfdRsIfPol``)."""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import EnabledDisabledChoices
from ...constants import COMMON_TENANT_NAME
from ..base import ACIBaseModel, ACITenantBaseModel


class ACIBFDInterfacePolicy(ACITenantBaseModel):
    """Reusable per-tenant BFD interface policy (``bfdIfPol``)."""

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="bfd_interface_policies",
        verbose_name=_("ACI Tenant"),
    )
    admin_state = models.CharField(
        verbose_name=_("Admin state"),
        max_length=16,
        default=EnabledDisabledChoices.ENABLED,
        choices=EnabledDisabledChoices,
    )
    detection_multiplier = models.PositiveSmallIntegerField(
        verbose_name=_("Detection multiplier"),
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
    )
    min_rx_interval_ms = models.PositiveSmallIntegerField(
        verbose_name=_("Min Rx interval (ms)"),
        default=50,
        validators=[MinValueValidator(50), MaxValueValidator(999)],
    )
    min_tx_interval_ms = models.PositiveSmallIntegerField(
        verbose_name=_("Min Tx interval (ms)"),
        default=50,
        validators=[MinValueValidator(50), MaxValueValidator(999)],
    )
    echo_admin_state = models.CharField(
        verbose_name=_("Echo admin state"),
        max_length=16,
        default=EnabledDisabledChoices.ENABLED,
        choices=EnabledDisabledChoices,
    )
    echo_rx_interval_ms = models.PositiveSmallIntegerField(
        verbose_name=_("Echo Rx interval (ms)"),
        default=50,
        validators=[MinValueValidator(50), MaxValueValidator(999)],
    )
    slow_timer_ms = models.PositiveIntegerField(
        verbose_name=_("Slow timer (ms)"),
        default=2000,
        validators=[MinValueValidator(1000), MaxValueValidator(10000)],
    )
    controls = models.JSONField(
        verbose_name=_("Controls"),
        default=list,
        blank=True,
        help_text=_("Tokens: optimize-subif, passive-mode."),
    )

    clone_fields = (
        "aci_tenant",
        "admin_state",
        "detection_multiplier",
        "min_rx_interval_ms",
        "min_tx_interval_ms",
        "echo_admin_state",
        "echo_rx_interval_ms",
        "slow_timer_ms",
        "description",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI BFD Interface Policy")
        verbose_name_plural = _("ACI BFD Interface Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_acibfdinterfacepolicy_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acibfdinterfacepolicy", args=[self.pk])


class ACIBFDInterfaceAttachment(ACIBaseModel):
    """BFD Interface Policy attached to a Logical Interface Profile."""

    aci_logical_interface_profile = models.OneToOneField(
        to="netbox_cisco_aci.ACILogicalInterfaceProfile",
        on_delete=models.CASCADE,
        related_name="bfd_attachment",
        verbose_name=_("Logical Interface Profile"),
    )
    aci_bfd_interface_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACIBFDInterfacePolicy",
        on_delete=models.PROTECT,
        related_name="attachments",
        verbose_name=_("BFD Interface Policy"),
    )

    clone_fields = (
        "aci_bfd_interface_policy",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI BFD Interface Attachment")
        verbose_name_plural = _("ACI BFD Interface Attachments")
        ordering = ("aci_logical_interface_profile",)

    def __str__(self) -> str:
        lip = self.aci_logical_interface_profile
        return f"{lip} BFD"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acibfdinterfaceattachment", args=[self.pk])

    def save(self, *args, **kwargs):
        # Auto-derive name from the logical interface profile if not provided.
        if not self.name and self.aci_logical_interface_profile_id:
            import re

            lip_name = getattr(self.aci_logical_interface_profile, "name", "")
            candidate = f"bfd_{lip_name}"
            candidate = re.sub(r"[^A-Za-z0-9._:\-]", "_", candidate)
            self.name = candidate[:64]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()

        # Cross-tenant guard: BFD policy tenant must match L3Out tenant or be `common`.
        if self.aci_bfd_interface_policy_id and self.aci_logical_interface_profile_id:
            policy_tenant_id = getattr(self.aci_bfd_interface_policy, "aci_tenant_id", None)
            lip = self.aci_logical_interface_profile
            l3out_tenant_id = getattr(
                getattr(getattr(lip, "aci_logical_node_profile", None), "aci_l3out", None),
                "aci_tenant_id",
                None,
            )
            if policy_tenant_id and l3out_tenant_id and policy_tenant_id != l3out_tenant_id:
                policy_tenant_name = getattr(self.aci_bfd_interface_policy.aci_tenant, "name", "")
                if policy_tenant_name != COMMON_TENANT_NAME:
                    raise ValidationError(
                        {
                            "aci_bfd_interface_policy": _(
                                "The BFD Interface Policy must belong to the same tenant "
                                "as the L3Out, or to the `common` tenant."
                            )
                        }
                    )
