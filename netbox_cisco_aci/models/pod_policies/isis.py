"""ACI IS-IS domain policy.

Maps APIC's ``isisDomPol``. Drives the IS-IS underlay between leaf and
spine fabric ports \u2014 LSP timers, metric style, fast-flood, etc.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import ISISMetricStyleChoices
from ._base import _PodPolicyBase


class ACIISISDomainPolicy(_PodPolicyBase):
    """IS-IS underlay policy for the fabric."""

    metric_style = models.CharField(
        verbose_name=_("Metric style"),
        max_length=8,
        choices=ISISMetricStyleChoices,
        default=ISISMetricStyleChoices.WIDE,
        help_text=_(
            "Wide metrics is the modern default and the only safe choice "
            "on ACI fabrics with more than \u224854 hops; ``narrow`` is kept "
            "for parity with the APIC enum."
        ),
    )
    lsp_fast_flood_enabled = models.BooleanField(
        verbose_name=_("LSP fast flood"),
        default=True,
        help_text=_("Enables LSP fast-flood for snappier convergence on link events."),
    )
    lsp_gen_init_intvl_ms = models.PositiveIntegerField(
        verbose_name=_("LSP gen init interval (ms)"),
        default=50,
        validators=[MinValueValidator(50), MaxValueValidator(120_000)],
    )
    lsp_gen_max_intvl_ms = models.PositiveIntegerField(
        verbose_name=_("LSP gen max interval (ms)"),
        default=8_000,
        validators=[MinValueValidator(50), MaxValueValidator(120_000)],
    )
    lsp_gen_sec_intvl_ms = models.PositiveIntegerField(
        verbose_name=_("LSP gen secondary interval (ms)"),
        default=50,
        validators=[MinValueValidator(50), MaxValueValidator(120_000)],
    )

    clone_fields = (
        "aci_fabric",
        "aci_tenant",
        "admin_state",
        "metric_style",
        "description",
    )

    class Meta(_PodPolicyBase.Meta):
        verbose_name = _("ACI IS-IS Domain Policy")
        verbose_name_plural = _("ACI IS-IS Domain Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                condition=models.Q(aci_tenant__isnull=True),
                name="netbox_cisco_aci_aciisis_fabric_name_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_fabric", "aci_tenant", "name"),
                condition=models.Q(aci_tenant__isnull=False),
                name="netbox_cisco_aci_aciisis_fabric_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        scope = self.aci_tenant.name if self.aci_tenant_id else "fabric"
        return f"{self.aci_fabric.name} / {scope} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciisisdomainpolicy", args=[self.pk])
