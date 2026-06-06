"""ACI NTP policy and its NTP providers.

Maps APIC's ``datetimeNtpPol`` and ``datetimeNtpProv`` MOs.
"""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import NTPProviderStateChoices
from ..base import ACIBaseModel
from ._base import _PodPolicyBase


class ACINTPPolicy(_PodPolicyBase):
    """NTP policy that lists upstream time servers for the fabric.

    Multiple providers can be associated. At most one provider per
    policy can be marked ``preferred`` (enforced by partial unique).
    """

    server_state_default = models.CharField(
        verbose_name=_("Default provider role"),
        max_length=16,
        choices=NTPProviderStateChoices,
        default=NTPProviderStateChoices.NORMAL,
        help_text=_(
            "Role assigned to a newly-added provider when no explicit "
            "role is given. Existing providers keep their stored role."
        ),
    )
    auth_state = models.BooleanField(
        verbose_name=_("Authentication enabled"),
        default=False,
        help_text=_(
            "When enabled, providers should reference a key_id and the "
            "fabric must have matching NTP keys configured out-of-band."
        ),
    )

    clone_fields = (
        "aci_fabric",
        "aci_tenant",
        "admin_state",
        "server_state_default",
        "description",
    )

    class Meta(_PodPolicyBase.Meta):
        verbose_name = _("ACI NTP Policy")
        verbose_name_plural = _("ACI NTP Policies")
        # PostgreSQL treats NULL values in unique columns as distinct
        # by default, so a single UniqueConstraint on
        # ``(aci_fabric, aci_tenant, name)`` would never fire for
        # fabric-wide rows where ``aci_tenant`` is NULL. Split into two
        # partial uniques — one per representation.
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                condition=models.Q(aci_tenant__isnull=True),
                name="netbox_cisco_aci_acintp_fabric_name_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_fabric", "aci_tenant", "name"),
                condition=models.Q(aci_tenant__isnull=False),
                name="netbox_cisco_aci_acintp_fabric_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        scope = self.aci_tenant.name if self.aci_tenant_id else "fabric"
        return f"{self.aci_fabric.name} / {scope} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acintppolicy", args=[self.pk])


class ACINTPProvider(ACIBaseModel):
    """One upstream NTP server within an ACINTPPolicy.

    The ``host`` field is a free-form CharField rather than an IPAM FK
    \u2014 NTP providers are often referenced by FQDN (e.g.
    ``time.cloudflare.com``), and APIC accepts either, so we mirror its
    free-form input style.
    """

    ntp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACINTPPolicy",
        on_delete=models.CASCADE,
        related_name="providers",
        verbose_name=_("NTP Policy"),
    )
    host = models.CharField(
        verbose_name=_("Host"),
        max_length=255,
        help_text=_("FQDN or IP address of the upstream NTP server."),
    )
    role = models.CharField(
        verbose_name=_("Role"),
        max_length=16,
        choices=NTPProviderStateChoices,
        default=NTPProviderStateChoices.NORMAL,
    )
    min_poll = models.PositiveSmallIntegerField(
        verbose_name=_("Min poll"),
        default=4,
        validators=[MinValueValidator(4), MaxValueValidator(16)],
        help_text=_("Minimum polling interval, log2 seconds (APIC range 4\u201316)."),
    )
    max_poll = models.PositiveSmallIntegerField(
        verbose_name=_("Max poll"),
        default=6,
        validators=[MinValueValidator(4), MaxValueValidator(16)],
        help_text=_("Maximum polling interval, log2 seconds (APIC range 4\u201316)."),
    )
    key_id = models.PositiveSmallIntegerField(
        verbose_name=_("Auth key ID"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        help_text=_("Optional authentication key ID. Secrets live on APIC, not here."),
    )
    mgmt_epg = models.CharField(
        verbose_name=_("Management EPG"),
        max_length=255,
        blank=True,
        help_text=_("Optional. e.g. 'default (Out-of-Band)' or 'inb-mgmt'."),
    )

    clone_fields = ("ntp_policy", "role", "min_poll", "max_poll", "mgmt_epg")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI NTP Provider")
        verbose_name_plural = _("ACI NTP Providers")
        constraints = (
            models.UniqueConstraint(
                fields=("ntp_policy", "host"),
                name="netbox_cisco_aci_acintpprov_policy_host_unique",
            ),
            # At most one preferred provider per policy.
            models.UniqueConstraint(
                fields=("ntp_policy",),
                condition=models.Q(role="preferred"),
                name="netbox_cisco_aci_acintpprov_policy_preferred_unique",
            ),
        )

    def clean(self) -> None:
        super().clean()
        if (
            self.min_poll is not None
            and self.max_poll is not None
            and self.min_poll > self.max_poll
        ):
            raise ValidationError(
                {"max_poll": _("Max poll must be greater than or equal to min poll.")}
            )

    def __str__(self) -> str:
        return f"{self.ntp_policy.name} / {self.host}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acintpprovider", args=[self.pk])
