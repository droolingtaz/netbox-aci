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
    # v0.4.0 — fabric-overlay control-plane bindings
    bgp_rr_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACIBGPRouteReflectorPolicy",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("BGP Route Reflector Policy"),
        null=True,
        blank=True,
    )
    coop_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACICOOPGroupPolicy",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("COOP Group Policy"),
        null=True,
        blank=True,
    )
    isis_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACIISISDomainPolicy",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("IS-IS Domain Policy"),
        null=True,
        blank=True,
    )
    # APIC's ``datetimePol`` MO is the same object as the NTP policy —
    # the pod-policy-group exposes one slot for clock + NTP. We point
    # this FK at the existing ACINTPPolicy rather than creating a
    # duplicate ACIDateTimePolicy model. Operators who want to keep
    # NTP and date/time conceptually separate can model two NTP
    # policies and bind each here.
    datetime_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACINTPPolicy",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Date/Time Policy"),
        null=True,
        blank=True,
        help_text=_(
            "APIC's date/time policy MO (datetimePol) is structurally the "
            "same as an NTP policy, so this slot points at an ACINTPPolicy."
        ),
    )

    clone_fields = (
        "aci_fabric",
        "ntp_policy",
        "syslog_policy",
        "snmp_policy",
        "snmp_trap_policy",
        "bgp_rr_policy",
        "coop_policy",
        "isis_policy",
        "datetime_policy",
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
