"""ACI Pod Policy Group — bundles NTP / Syslog / SNMP / SNMP-Trap policies.

Maps APIC's ``fabricPodPGrp`` MO. In APIC the Pod Policy Group is the
object actually *applied* to a Pod via a Pod Selector; the individual
NTP / Syslog / SNMP policies are just references that the group ties
together. We model it as a fabric-scoped object with one optional FK
per protocol so a single binding row can be cloned and re-pointed.
"""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACIFabricBaseModel


class ACIPodPolicyGroup(ACIFabricBaseModel):
    """A pod-policy-group binding row."""

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="pod_policy_groups",
        verbose_name=_("ACI Fabric"),
    )
    ntp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACINTPPolicy",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("NTP Policy"),
        null=True,
        blank=True,
    )
    syslog_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISyslogPolicy",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Syslog Policy"),
        null=True,
        blank=True,
    )
    snmp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISNMPPolicy",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("SNMP Policy"),
        null=True,
        blank=True,
    )
    snmp_trap_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISNMPTrapPolicy",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("SNMP Trap Policy"),
        null=True,
        blank=True,
    )

    clone_fields = (
        "aci_fabric",
        "ntp_policy",
        "syslog_policy",
        "snmp_policy",
        "snmp_trap_policy",
        "description",
    )

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Pod Policy Group")
        verbose_name_plural = _("ACI Pod Policy Groups")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acipodpolicygrp_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acipodpolicygroup", args=[self.pk])
