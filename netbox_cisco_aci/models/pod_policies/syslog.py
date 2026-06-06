"""ACI Syslog policy and its remote destinations.

Maps APIC's ``syslogGroup`` (parent) and ``syslogRemoteDest`` (child).
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import (
    EnabledDisabledChoices,
    SyslogFacilityChoices,
    SyslogSeverityChoices,
)
from ..base import ACIBaseModel
from ._base import _PodPolicyBase


class ACISyslogPolicy(_PodPolicyBase):
    """Syslog policy: console + local file + remote forwarding container."""

    console_severity = models.CharField(
        verbose_name=_("Console severity"),
        max_length=16,
        choices=SyslogSeverityChoices,
        default=SyslogSeverityChoices.CRITICAL,
        help_text=_("Severity threshold for the on-switch console."),
    )
    local_severity = models.CharField(
        verbose_name=_("Local file severity"),
        max_length=16,
        choices=SyslogSeverityChoices,
        default=SyslogSeverityChoices.INFORMATION,
        help_text=_("Severity threshold written to local log files on each node."),
    )
    include_msec = models.BooleanField(
        verbose_name=_("Include msec in timestamp"),
        default=True,
    )
    include_tz = models.BooleanField(
        verbose_name=_("Include timezone in timestamp"),
        default=True,
    )

    clone_fields = (
        "aci_fabric",
        "aci_tenant",
        "admin_state",
        "console_severity",
        "local_severity",
        "description",
    )

    class Meta(_PodPolicyBase.Meta):
        verbose_name = _("ACI Syslog Policy")
        verbose_name_plural = _("ACI Syslog Policies")
        # See ACINTPPolicy.Meta for why uniqueness is split across two
        # partial constraints on the nullable ``aci_tenant`` column.
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                condition=models.Q(aci_tenant__isnull=True),
                name="netbox_cisco_aci_acisyslog_fabric_name_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_fabric", "aci_tenant", "name"),
                condition=models.Q(aci_tenant__isnull=False),
                name="netbox_cisco_aci_acisyslog_fabric_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        scope = self.aci_tenant.name if self.aci_tenant_id else "fabric"
        return f"{self.aci_fabric.name} / {scope} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisyslogpolicy", args=[self.pk])


class ACISyslogRemoteDest(ACIBaseModel):
    """One remote syslog forwarding destination inside a syslog policy."""

    syslog_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISyslogPolicy",
        on_delete=models.CASCADE,
        related_name="remote_destinations",
        verbose_name=_("Syslog Policy"),
    )
    host = models.CharField(
        verbose_name=_("Host"),
        max_length=255,
        help_text=_("FQDN or IP of the remote syslog collector."),
    )
    port = models.PositiveIntegerField(
        verbose_name=_("Port"),
        default=514,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    severity = models.CharField(
        verbose_name=_("Severity"),
        max_length=16,
        choices=SyslogSeverityChoices,
        default=SyslogSeverityChoices.WARNINGS,
        help_text=_("Severity threshold for messages forwarded to this destination."),
    )
    forwarding_facility = models.CharField(
        verbose_name=_("Forwarding facility"),
        max_length=16,
        choices=SyslogFacilityChoices,
        default=SyslogFacilityChoices.LOCAL7,
    )
    admin_state = models.CharField(
        verbose_name=_("Admin state"),
        max_length=16,
        choices=EnabledDisabledChoices,
        default=EnabledDisabledChoices.ENABLED,
    )
    mgmt_epg = models.CharField(
        verbose_name=_("Management EPG"),
        max_length=255,
        blank=True,
    )

    clone_fields = (
        "syslog_policy",
        "port",
        "severity",
        "forwarding_facility",
        "admin_state",
        "mgmt_epg",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Syslog Remote Destination")
        verbose_name_plural = _("ACI Syslog Remote Destinations")
        constraints = (
            models.UniqueConstraint(
                fields=("syslog_policy", "host", "port"),
                name="netbox_cisco_aci_acisyslogdest_policy_host_port_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.syslog_policy.name} / {self.host}:{self.port}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisyslogremotedest", args=[self.pk])
