"""Model-level tests for v0.3.0: Pod Policies (NTP / Syslog / SNMP / Traps).

Coverage targets:

- Per-fabric+tenant uniqueness on every policy parent.
- Per-policy uniqueness on every child (provider, destination, etc.).
- The "at most one preferred NTP provider per policy" partial unique.
- ``clean()`` rejections (NTP min/max poll ordering, trap v3-security
  only when version=v3).
- ``display_gateway``-style scope rendering on policy __str__.
"""

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from netbox_cisco_aci.choices import (
    NTPProviderStateChoices,
    SNMPSecurityLevelChoices,
    SNMPVersionChoices,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.pod_policies import (
    ACINTPPolicy,
    ACINTPProvider,
    ACIPodPolicyGroup,
    ACISNMPClient,
    ACISNMPClientGroup,
    ACISNMPCommunity,
    ACISNMPPolicy,
    ACISNMPTrapDest,
    ACISNMPTrapPolicy,
    ACISNMPv3User,
    ACISyslogPolicy,
    ACISyslogRemoteDest,
)
from netbox_cisco_aci.models.tenant import ACITenant


class _PodPolicyFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fabric = ACIFabric.objects.create(name="DC1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fabric, name="acme")


# ---------------------------------------------------------------------------
# NTP
# ---------------------------------------------------------------------------


class ACINTPPolicyTests(_PodPolicyFixture):
    def test_fabric_wide_and_tenant_scoped_can_share_name(self):
        """A fabric-wide policy and a tenant-scoped one may share a name."""
        ACINTPPolicy.objects.create(aci_fabric=self.fabric, name="default")
        # Same name, scoped to a tenant — allowed because aci_tenant differs.
        ACINTPPolicy.objects.create(aci_fabric=self.fabric, aci_tenant=self.tenant, name="default")

    def test_unique_inside_same_scope(self):
        ACINTPPolicy.objects.create(aci_fabric=self.fabric, name="default")
        with self.assertRaises(IntegrityError):
            ACINTPPolicy.objects.create(aci_fabric=self.fabric, name="default")

    def test_str_renders_scope(self):
        fabric_wide = ACINTPPolicy.objects.create(aci_fabric=self.fabric, name="fw")
        tenant_scoped = ACINTPPolicy.objects.create(
            aci_fabric=self.fabric, aci_tenant=self.tenant, name="ts"
        )
        self.assertIn("fabric", str(fabric_wide))
        self.assertIn(self.tenant.name, str(tenant_scoped))


class ACINTPProviderTests(_PodPolicyFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policy = ACINTPPolicy.objects.create(aci_fabric=cls.fabric, name="ntp")

    def test_host_unique_inside_policy(self):
        ACINTPProvider.objects.create(ntp_policy=self.policy, host="10.0.0.1", name="p1")
        with self.assertRaises(IntegrityError):
            ACINTPProvider.objects.create(ntp_policy=self.policy, host="10.0.0.1", name="p2")

    def test_only_one_preferred_per_policy(self):
        ACINTPProvider.objects.create(
            ntp_policy=self.policy,
            host="10.0.0.1",
            name="p1",
            role=NTPProviderStateChoices.PREFERRED,
        )
        with self.assertRaises(IntegrityError):
            ACINTPProvider.objects.create(
                ntp_policy=self.policy,
                host="10.0.0.2",
                name="p2",
                role=NTPProviderStateChoices.PREFERRED,
            )

    def test_min_poll_must_be_le_max_poll(self):
        prov = ACINTPProvider(
            ntp_policy=self.policy, host="10.0.0.1", name="bad", min_poll=10, max_poll=6
        )
        with self.assertRaises(ValidationError):
            prov.full_clean()


# ---------------------------------------------------------------------------
# Syslog
# ---------------------------------------------------------------------------


class ACISyslogPolicyTests(_PodPolicyFixture):
    def test_unique_inside_scope(self):
        ACISyslogPolicy.objects.create(aci_fabric=self.fabric, name="syslog")
        with self.assertRaises(IntegrityError):
            ACISyslogPolicy.objects.create(aci_fabric=self.fabric, name="syslog")


class ACISyslogRemoteDestTests(_PodPolicyFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policy = ACISyslogPolicy.objects.create(aci_fabric=cls.fabric, name="syslog")

    def test_host_port_unique_inside_policy(self):
        ACISyslogRemoteDest.objects.create(
            syslog_policy=self.policy, host="10.0.0.10", port=514, name="d1"
        )
        with self.assertRaises(IntegrityError):
            ACISyslogRemoteDest.objects.create(
                syslog_policy=self.policy, host="10.0.0.10", port=514, name="d2"
            )

    def test_same_host_different_port_allowed(self):
        ACISyslogRemoteDest.objects.create(
            syslog_policy=self.policy, host="10.0.0.10", port=514, name="d1"
        )
        ACISyslogRemoteDest.objects.create(
            syslog_policy=self.policy, host="10.0.0.10", port=6514, name="d2"
        )


# ---------------------------------------------------------------------------
# SNMP
# ---------------------------------------------------------------------------


class ACISNMPPolicyTests(_PodPolicyFixture):
    def test_unique_inside_scope(self):
        ACISNMPPolicy.objects.create(aci_fabric=self.fabric, name="snmp")
        with self.assertRaises(IntegrityError):
            ACISNMPPolicy.objects.create(aci_fabric=self.fabric, name="snmp")


class ACISNMPChildrenTests(_PodPolicyFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policy = ACISNMPPolicy.objects.create(aci_fabric=cls.fabric, name="snmp")

    def test_community_name_unique_per_policy(self):
        ACISNMPCommunity.objects.create(snmp_policy=self.policy, name="public")
        with self.assertRaises(IntegrityError):
            ACISNMPCommunity.objects.create(snmp_policy=self.policy, name="public")

    def test_client_group_name_unique_per_policy(self):
        ACISNMPClientGroup.objects.create(snmp_policy=self.policy, name="ops")
        with self.assertRaises(IntegrityError):
            ACISNMPClientGroup.objects.create(snmp_policy=self.policy, name="ops")

    def test_client_address_unique_per_group(self):
        grp = ACISNMPClientGroup.objects.create(snmp_policy=self.policy, name="ops")
        ACISNMPClient.objects.create(client_group=grp, address="10.0.0.0/24", name="lan")
        with self.assertRaises(IntegrityError):
            ACISNMPClient.objects.create(client_group=grp, address="10.0.0.0/24", name="lan-dup")

    def test_v3_user_name_unique_per_policy(self):
        ACISNMPv3User.objects.create(snmp_policy=self.policy, name="ops-user")
        with self.assertRaises(IntegrityError):
            ACISNMPv3User.objects.create(snmp_policy=self.policy, name="ops-user")


# ---------------------------------------------------------------------------
# SNMP Traps
# ---------------------------------------------------------------------------


class ACISNMPTrapPolicyTests(_PodPolicyFixture):
    def test_unique_inside_scope(self):
        ACISNMPTrapPolicy.objects.create(aci_fabric=self.fabric, name="traps")
        with self.assertRaises(IntegrityError):
            ACISNMPTrapPolicy.objects.create(aci_fabric=self.fabric, name="traps")


class ACISNMPTrapDestTests(_PodPolicyFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policy = ACISNMPTrapPolicy.objects.create(aci_fabric=cls.fabric, name="traps")

    def test_host_port_unique_inside_policy(self):
        ACISNMPTrapDest.objects.create(
            trap_policy=self.policy, host="10.0.0.20", port=162, name="d1"
        )
        with self.assertRaises(IntegrityError):
            ACISNMPTrapDest.objects.create(
                trap_policy=self.policy, host="10.0.0.20", port=162, name="d2"
            )

    def test_v3_security_only_on_v3_traps(self):
        dest = ACISNMPTrapDest(
            trap_policy=self.policy,
            host="10.0.0.20",
            name="bad",
            version=SNMPVersionChoices.V2C,
            v3_security_level=SNMPSecurityLevelChoices.AUTH_PRIV,
        )
        with self.assertRaises(ValidationError):
            dest.full_clean()

    def test_v3_security_allowed_on_v3_traps(self):
        ACISNMPTrapDest(
            trap_policy=self.policy,
            host="10.0.0.21",
            name="good",
            version=SNMPVersionChoices.V3,
            v3_security_level=SNMPSecurityLevelChoices.AUTH_PRIV,
        ).full_clean()

    def test_v2c_with_blank_security_level_is_fine(self):
        ACISNMPTrapDest(
            trap_policy=self.policy,
            host="10.0.0.22",
            name="v2c",
            version=SNMPVersionChoices.V2C,
        ).full_clean()


# ---------------------------------------------------------------------------
# Pod Policy Group
# ---------------------------------------------------------------------------


class ACIPodPolicyGroupTests(_PodPolicyFixture):
    def test_unique_name_per_fabric(self):
        ACIPodPolicyGroup.objects.create(aci_fabric=self.fabric, name="default")
        with self.assertRaises(IntegrityError):
            ACIPodPolicyGroup.objects.create(aci_fabric=self.fabric, name="default")

    def test_same_name_different_fabric_allowed(self):
        other = ACIFabric.objects.create(name="DC2")
        ACIPodPolicyGroup.objects.create(aci_fabric=self.fabric, name="default")
        ACIPodPolicyGroup.objects.create(aci_fabric=other, name="default")

    def test_bound_policies_round_trip(self):
        ntp = ACINTPPolicy.objects.create(aci_fabric=self.fabric, name="ntp")
        syslog = ACISyslogPolicy.objects.create(aci_fabric=self.fabric, name="syslog")
        snmp = ACISNMPPolicy.objects.create(aci_fabric=self.fabric, name="snmp")
        traps = ACISNMPTrapPolicy.objects.create(aci_fabric=self.fabric, name="traps")
        grp = ACIPodPolicyGroup.objects.create(
            aci_fabric=self.fabric,
            name="pg1",
            ntp_policy=ntp,
            syslog_policy=syslog,
            snmp_policy=snmp,
            snmp_trap_policy=traps,
        )
        grp.refresh_from_db()
        self.assertEqual(grp.ntp_policy_id, ntp.pk)
        self.assertEqual(grp.syslog_policy_id, syslog.pk)
        self.assertEqual(grp.snmp_policy_id, snmp.pk)
        self.assertEqual(grp.snmp_trap_policy_id, traps.pk)

    def test_policy_set_null_on_delete(self):
        ntp = ACINTPPolicy.objects.create(aci_fabric=self.fabric, name="ntp")
        grp = ACIPodPolicyGroup.objects.create(aci_fabric=self.fabric, name="pg2", ntp_policy=ntp)
        ntp.delete()
        grp.refresh_from_db()
        self.assertIsNone(grp.ntp_policy_id)
