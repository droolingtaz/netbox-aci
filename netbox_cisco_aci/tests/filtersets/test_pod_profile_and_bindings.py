"""FilterSet search() tests for v0.4.0 Pod Profile + extended bindings."""

from django.test import TestCase

from netbox_cisco_aci.filtersets.pod_policies import (
    ACIBGPRouteReflectorNodeFilterSet,
    ACIBGPRouteReflectorPolicyFilterSet,
    ACICOOPGroupPolicyFilterSet,
    ACIISISDomainPolicyFilterSet,
    ACIPodProfileFilterSet,
    ACIPodSelectorFilterSet,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.pod_policies import (
    ACIBGPRouteReflectorNode,
    ACIBGPRouteReflectorPolicy,
    ACICOOPGroupPolicy,
    ACIISISDomainPolicy,
    ACIPodPolicyGroup,
    ACIPodProfile,
    ACIPodSelector,
)


class _Fixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="search-fab")


class ACIBGPRouteReflectorPolicySearchTests(_Fixture):
    def test_name_match(self):
        ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=self.fab, name="bgp-rr-alpha", autonomous_system_number=65000
        )
        qs = ACIBGPRouteReflectorPolicyFilterSet(
            {"q": "alpha"}, queryset=ACIBGPRouteReflectorPolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)


class ACIBGPRouteReflectorNodeSearchTests(_Fixture):
    def test_name_match(self):
        pol = ACIBGPRouteReflectorPolicy.objects.create(
            aci_fabric=self.fab, name="rr", autonomous_system_number=65000
        )
        ACIBGPRouteReflectorNode.objects.create(bgp_rr_policy=pol, node_id=201, name="spine-201")
        qs = ACIBGPRouteReflectorNodeFilterSet(
            {"q": "spine"}, queryset=ACIBGPRouteReflectorNode.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)


class ACICOOPGroupPolicySearchTests(_Fixture):
    def test_filterset_search_returns_match(self):
        ACICOOPGroupPolicy.objects.create(aci_fabric=self.fab, name="coop-strict")
        qs = ACICOOPGroupPolicyFilterSet(
            {"q": "strict"}, queryset=ACICOOPGroupPolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)


class ACIISISDomainPolicySearchTests(_Fixture):
    def test_filterset_search_returns_match(self):
        ACIISISDomainPolicy.objects.create(aci_fabric=self.fab, name="isis-wide")
        qs = ACIISISDomainPolicyFilterSet(
            {"q": "wide"}, queryset=ACIISISDomainPolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)


class ACIPodProfileSearchTests(_Fixture):
    def test_name_match(self):
        ACIPodProfile.objects.create(aci_fabric=self.fab, name="default-profile")
        qs = ACIPodProfileFilterSet({"q": "default"}, queryset=ACIPodProfile.objects.all()).qs
        self.assertEqual(qs.count(), 1)


class ACIPodSelectorSearchTests(_Fixture):
    def test_name_match(self):
        profile = ACIPodProfile.objects.create(aci_fabric=self.fab, name="default")
        ppg = ACIPodPolicyGroup.objects.create(aci_fabric=self.fab, name="pg")
        ACIPodSelector.objects.create(
            pod_profile=profile,
            name="all-pods",
            selector_type="all",
            pod_policy_group=ppg,
        )
        qs = ACIPodSelectorFilterSet({"q": "all-pods"}, queryset=ACIPodSelector.objects.all()).qs
        self.assertEqual(qs.count(), 1)
