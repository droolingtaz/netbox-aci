"""ACI Pod Profile + Pod Selector.

Maps APIC's ``fabricPodP`` (Pod Profile) and ``fabricPodS`` (Pod
Selector). A Pod Profile sits at the fabric scope and contains one or
more Pod Selectors; each selector targets a range of pod IDs (or
``ALL``) and points at exactly one :class:`ACIPodPolicyGroup`. This is
the binding layer that actually applies a pod-policy-group to a pod.
"""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import RangeAllChoices
from ...constants import POD_ID_MAX, POD_ID_MIN
from ..base import ACIBaseModel, ACIFabricBaseModel


class ACIPodProfile(ACIFabricBaseModel):
    """A Pod Profile (``fabricPodP``).

    APIC ships exactly one Pod Profile per fabric, named ``default``,
    but we don't enforce that \u2014 multi-pod operators sometimes maintain
    parallel profiles during migrations.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="pod_profiles",
        verbose_name=_("ACI Fabric"),
    )

    clone_fields = ("aci_fabric", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Pod Profile")
        verbose_name_plural = _("ACI Pod Profiles")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acipodprofile_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acipodprofile", args=[self.pk])


class ACIPodSelector(ACIBaseModel):
    """A Pod Selector inside a Pod Profile (``fabricPodS``).

    Selectors are either ``ALL`` (apply to every pod) or ``RANGE`` (apply
    to pod IDs ``pod_block_from``\u2026``pod_block_to`` inclusive). Each
    selector points at exactly one :class:`ACIPodPolicyGroup`.
    """

    pod_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACIPodProfile",
        on_delete=models.CASCADE,
        related_name="selectors",
        verbose_name=_("Pod Profile"),
    )
    selector_type = models.CharField(
        verbose_name=_("Selector type"),
        max_length=8,
        choices=RangeAllChoices,
        default=RangeAllChoices.RANGE,
    )
    pod_block_from = models.PositiveSmallIntegerField(
        verbose_name=_("Pod block: from"),
        null=True,
        blank=True,
        validators=[MinValueValidator(POD_ID_MIN), MaxValueValidator(POD_ID_MAX)],
        help_text=_("Lower bound (inclusive). Required when selector_type=range."),
    )
    pod_block_to = models.PositiveSmallIntegerField(
        verbose_name=_("Pod block: to"),
        null=True,
        blank=True,
        validators=[MinValueValidator(POD_ID_MIN), MaxValueValidator(POD_ID_MAX)],
        help_text=_("Upper bound (inclusive). Required when selector_type=range."),
    )
    pod_policy_group = models.ForeignKey(
        to="netbox_cisco_aci.ACIPodPolicyGroup",
        on_delete=models.PROTECT,
        related_name="selectors",
        verbose_name=_("Pod Policy Group"),
        help_text=_("The pod-policy-group that pods matched by this selector receive."),
    )

    clone_fields = (
        "pod_profile",
        "selector_type",
        "pod_policy_group",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Pod Selector")
        verbose_name_plural = _("ACI Pod Selectors")
        constraints = (
            models.UniqueConstraint(
                fields=("pod_profile", "name"),
                name="netbox_cisco_aci_acipodselector_profile_name_unique",
            ),
        )

    def clean(self) -> None:
        super().clean()
        if self.selector_type == RangeAllChoices.RANGE:
            if self.pod_block_from is None or self.pod_block_to is None:
                raise ValidationError(
                    {
                        "pod_block_from": _(
                            "Range selectors must specify both pod_block_from and pod_block_to."
                        )
                    }
                )
            if self.pod_block_from > self.pod_block_to:
                raise ValidationError(
                    {"pod_block_to": _("pod_block_to must be >= pod_block_from.")}
                )
        else:  # ALL
            if self.pod_block_from is not None or self.pod_block_to is not None:
                raise ValidationError(
                    {
                        "pod_block_from": _(
                            "ALL selectors must leave pod_block_from / pod_block_to blank."
                        )
                    }
                )

    def __str__(self) -> str:
        if self.selector_type == RangeAllChoices.ALL:
            scope = "ALL"
        else:
            scope = f"{self.pod_block_from}\u2013{self.pod_block_to}"
        return f"{self.pod_profile.name} / {self.name} ({scope})"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acipodselector", args=[self.pk])
