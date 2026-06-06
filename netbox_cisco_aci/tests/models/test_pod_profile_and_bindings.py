"""Model-level tests for v0.4.0:

- BGP Route Reflector policy + its spine-node child.
- COOP Group policy.
- IS-IS Domain policy.
- Pod Profile + Pod Selector.
- Extended fabric-overlay bindings on ACIPodPolicyGroup (4 new FKs).
"""

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from netbox_cisco_aci.choices import RangeAllChoices
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.pod_policies import (
    ACIBGPRouteReflectorNode,
    ACIBGPRouteReflectorPolicy,
    ACICOOPGroupPolicy,
    ACIISISDomainPolicy,
    ACINTPPolicy,
    ACIPodPolicyGroup,
    ACIPodProfile,
    ACIPodSelector,
)
from netbox_cisco_aci.models.tenant import ACITenant


class _Fixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fabric = ACIFabric.objects.create(name="DC1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fabric, name="acme")


# ---------------------------------------------------------------------------
# BGP Route Reflector
# ---------------------------------------------------------------------------


class ACIBGPRouteReflectorPolicyTests(_Fixture):
    def test_fabric_wide_and_tenant_scoped_can_share_name(self):
        ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=self.fabric, name="default", autonomous_system_number=65000
        )
        ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=self.fabric,
            aci_tenant=self.tenant,
            name="default",
            autonomous_system_number=65000,
        )

    def test_unique_inside_same_scope(self):
        ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=self.fabric, name="default", autonomous_system_number=65000
        )
        with self.assertRaises(IntegrityError):
            ACIBGPRouteReflectorPolicy.objects.create(
                aci_fabric=self.fabric, name="default", autonomous_system_number=65000
            )

    def test_asn_must_be_positive(self):
        pol = ACIBGPRouteReflectorPolicy(
            aci_fabric=self.fabric, name="bad", autonomous_system_number=0
        )
        with self.assertRaises(ValidationError):
            pol.full_clean()


class ACIBGPRouteReflectorNodeTests(_Fixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policy = ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=cls.fabric, name="default", autonomous_system_number=65001
        )

    def test_node_id_unique_inside_policy(self):
        ACIBGPRouteReflectorNode.objects.create(
            bgp_rr_policy=self.policy, node_id=201, name="spine-201"
        )
        with self.assertRaises(IntegrityError):
            ACIBGPRouteReflectorNode.objects.create(
                bgp_rr_policy=self.policy, node_id=201, name="spine-201-dup"
            )

    def test_same_node_id_different_policy_allowed(self):
        other = ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=self.fabric, name="other", autonomous_system_number=65002
        )
        ACIBGPRouteReflectorNode.objects.create(
            bgp_rr_policy=self.policy, node_id=201, name="spine-a"
        )
        ACIBGPRouteReflectorNode.objects.create(bgp_rr_policy=other, node_id=201, name="spine-b")


# ---------------------------------------------------------------------------
# COOP + IS-IS
# ---------------------------------------------------------------------------


class ACICOOPGroupPolicyTests(_Fixture):
    def test_unique_inside_scope(self):
        ACICOOPGroupPolicy.objects.create(aci_fabric=self.fabric, name="coop")
        with self.assertRaises(IntegrityError):
            ACICOOPGroupPolicy.objects.create(aci_fabric=self.fabric, name="coop")


class ACIISISDomainPolicyTests(_Fixture):
    def test_unique_inside_scope(self):
        ACIISISDomainPolicy.objects.create(aci_fabric=self.fabric, name="isis")
        with self.assertRaises(IntegrityError):
            ACIISISDomainPolicy.objects.create(aci_fabric=self.fabric, name="isis")

    def test_lsp_interval_min_value_enforced(self):
        pol = ACIISISDomainPolicy(
            aci_fabric=self.fabric,
            name="bad",
            lsp_gen_init_intvl_ms=10,  # < 50 minimum
        )
        with self.assertRaises(ValidationError):
            pol.full_clean()


# ---------------------------------------------------------------------------
# Pod Profile + Pod Selector
# ---------------------------------------------------------------------------


class ACIPodProfileTests(_Fixture):
    def test_unique_name_per_fabric(self):
        ACIPodProfile.objects.create(aci_fabric=self.fabric, name="default")
        with self.assertRaises(IntegrityError):
            ACIPodProfile.objects.create(aci_fabric=self.fabric, name="default")

    def test_same_name_different_fabric_allowed(self):
        other = ACIFabric.objects.create(name="DC2")
        ACIPodProfile.objects.create(aci_fabric=self.fabric, name="default")
        ACIPodProfile.objects.create(aci_fabric=other, name="default")


class ACIPodSelectorTests(_Fixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.profile = ACIPodProfile.objects.create(aci_fabric=cls.fabric, name="default")
        cls.ppg = ACIPodPolicyGroup.objects.create(aci_fabric=cls.fabric, name="pg")

    def test_range_selector_requires_from_and_to(self):
        sel = ACIPodSelector(
            pod_profile=self.profile,
            name="bad",
            selector_type=RangeAllChoices.RANGE,
            pod_policy_group=self.ppg,
        )
        with self.assertRaises(ValidationError):
            sel.full_clean()

    def test_range_selector_from_must_be_le_to(self):
        sel = ACIPodSelector(
            pod_profile=self.profile,
            name="bad",
            selector_type=RangeAllChoices.RANGE,
            pod_block_from=5,
            pod_block_to=3,
            pod_policy_group=self.ppg,
        )
        with self.assertRaises(ValidationError):
            sel.full_clean()

    def test_all_selector_must_leave_block_blank(self):
        sel = ACIPodSelector(
            pod_profile=self.profile,
            name="bad",
            selector_type=RangeAllChoices.ALL,
            pod_block_from=1,
            pod_block_to=10,
            pod_policy_group=self.ppg,
        )
        with self.assertRaises(ValidationError):
            sel.full_clean()

    def test_all_selector_clean_passes_with_blanks(self):
        ACIPodSelector(
            pod_profile=self.profile,
            name="all",
            selector_type=RangeAllChoices.ALL,
            pod_policy_group=self.ppg,
        ).full_clean()

    def test_range_selector_clean_passes_with_valid_block(self):
        ACIPodSelector(
            pod_profile=self.profile,
            name="r",
            selector_type=RangeAllChoices.RANGE,
            pod_block_from=1,
            pod_block_to=4,
            pod_policy_group=self.ppg,
        ).full_clean()

    def test_selector_name_unique_per_profile(self):
        ACIPodSelector.objects.create(
            pod_profile=self.profile,
            name="all",
            selector_type=RangeAllChoices.ALL,
            pod_policy_group=self.ppg,
        )
        with self.assertRaises(IntegrityError):
            ACIPodSelector.objects.create(
                pod_profile=self.profile,
                name="all",
                selector_type=RangeAllChoices.ALL,
                pod_policy_group=self.ppg,
            )


# ---------------------------------------------------------------------------
# Extended ACIPodPolicyGroup bindings
# ---------------------------------------------------------------------------


class ACIPodPolicyGroupExtendedBindingsTests(_Fixture):
    def test_bind_all_four_new_slots(self):
        bgp = ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=self.fabric, name="rr", autonomous_system_number=65000
        )
        coop = ACICOOPGroupPolicy.objects.create(aci_fabric=self.fabric, name="coop")
        isis = ACIISISDomainPolicy.objects.create(aci_fabric=self.fabric, name="isis")
        dt = ACINTPPolicy.objects.create(aci_fabric=self.fabric, name="dt")
        ppg = ACIPodPolicyGroup.objects.create(
            aci_fabric=self.fabric,
            name="pg",
            bgp_rr_policy=bgp,
            coop_policy=coop,
            isis_policy=isis,
            datetime_policy=dt,
        )
        ppg.refresh_from_db()
        self.assertEqual(ppg.bgp_rr_policy_id, bgp.pk)
        self.assertEqual(ppg.coop_policy_id, coop.pk)
        self.assertEqual(ppg.isis_policy_id, isis.pk)
        self.assertEqual(ppg.datetime_policy_id, dt.pk)

    def test_set_null_on_delete_for_each_new_fk(self):
        bgp = ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=self.fabric, name="rr", autonomous_system_number=65000
        )
        coop = ACICOOPGroupPolicy.objects.create(aci_fabric=self.fabric, name="coop")
        isis = ACIISISDomainPolicy.objects.create(aci_fabric=self.fabric, name="isis")
        dt = ACINTPPolicy.objects.create(aci_fabric=self.fabric, name="dt")
        ppg = ACIPodPolicyGroup.objects.create(
            aci_fabric=self.fabric,
            name="pg",
            bgp_rr_policy=bgp,
            coop_policy=coop,
            isis_policy=isis,
            datetime_policy=dt,
        )
        bgp.delete()
        coop.delete()
        isis.delete()
        dt.delete()
        ppg.refresh_from_db()
        self.assertIsNone(ppg.bgp_rr_policy_id)
        self.assertIsNone(ppg.coop_policy_id)
        self.assertIsNone(ppg.isis_policy_id)
        self.assertIsNone(ppg.datetime_policy_id)
