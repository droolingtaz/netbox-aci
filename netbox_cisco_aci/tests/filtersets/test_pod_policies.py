"""FilterSet search() tests for v0.3.0 Pod Policies."""

from django.test import TestCase

from netbox_cisco_aci.filtersets.pod_policies import (
    ACINTPPolicyFilterSet,
    ACINTPProviderFilterSet,
    ACIPodPolicyGroupFilterSet,
    ACISNMPClientFilterSet,
    ACISNMPClientGroupFilterSet,
    ACISNMPCommunityFilterSet,
    ACISNMPPolicyFilterSet,
    ACISNMPTrapDestFilterSet,
    ACISNMPTrapPolicyFilterSet,
    ACISNMPv3UserFilterSet,
    ACISyslogPolicyFilterSet,
    ACISyslogRemoteDestFilterSet,
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


class _Fixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="search-fab")


class ACINTPPolicySearchTests(_Fixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.a = ACINTPPolicy.objects.create(aci_fabric=cls.fab, name="alpha-ntp")
        cls.b = ACINTPPolicy.objects.create(
            aci_fabric=cls.fab, name="beta-ntp", description="alpha in description"
        )

    def test_name_match(self):
        qs = ACINTPPolicyFilterSet({"q": "alpha"}, queryset=ACINTPPolicy.objects.all()).qs
        self.assertEqual(set(qs), {self.a, self.b})

    def test_no_match_returns_empty(self):
        qs = ACINTPPolicyFilterSet({"q": "zzz"}, queryset=ACINTPPolicy.objects.all()).qs
        self.assertFalse(qs.exists())


class ACINTPProviderSearchTests(_Fixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policy = ACINTPPolicy.objects.create(aci_fabric=cls.fab, name="ntp")
        cls.p1 = ACINTPProvider.objects.create(
            ntp_policy=cls.policy, host="time1.example.com", name="p1"
        )
        cls.p2 = ACINTPProvider.objects.create(
            ntp_policy=cls.policy, host="10.0.0.1", name="p2", description="time1"
        )

    def test_host_match(self):
        qs = ACINTPProviderFilterSet({"q": "time1"}, queryset=ACINTPProvider.objects.all()).qs
        self.assertEqual(set(qs), {self.p1, self.p2})


class ACISyslogPolicySearchTests(_Fixture):
    def test_filterset_search_returns_match(self):
        ACISyslogPolicy.objects.create(aci_fabric=self.fab, name="syslog-alpha")
        qs = ACISyslogPolicyFilterSet({"q": "alpha"}, queryset=ACISyslogPolicy.objects.all()).qs
        self.assertEqual(qs.count(), 1)


class ACISyslogRemoteDestSearchTests(_Fixture):
    def test_host_search(self):
        pol = ACISyslogPolicy.objects.create(aci_fabric=self.fab, name="syslog")
        d = ACISyslogRemoteDest.objects.create(
            syslog_policy=pol, host="logs.example.com", name="d1"
        )
        qs = ACISyslogRemoteDestFilterSet(
            {"q": "logs"}, queryset=ACISyslogRemoteDest.objects.all()
        ).qs
        self.assertEqual(list(qs), [d])


class ACISNMPPolicySearchTests(_Fixture):
    def test_contact_and_location_searchable(self):
        ACISNMPPolicy.objects.create(
            aci_fabric=self.fab, name="snmp", contact="netops@example.com", location="DC1"
        )
        for query in ("netops", "DC1"):
            qs = ACISNMPPolicyFilterSet({"q": query}, queryset=ACISNMPPolicy.objects.all()).qs
            self.assertEqual(qs.count(), 1, msg=f"query={query!r}")


class ACISNMPCommunitySearchTests(_Fixture):
    def test_name_search(self):
        pol = ACISNMPPolicy.objects.create(aci_fabric=self.fab, name="snmp")
        ACISNMPCommunity.objects.create(snmp_policy=pol, name="readonly")
        qs = ACISNMPCommunityFilterSet(
            {"q": "readonly"}, queryset=ACISNMPCommunity.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)


class ACISNMPClientGroupSearchTests(_Fixture):
    def test_mgmt_epg_match(self):
        pol = ACISNMPPolicy.objects.create(aci_fabric=self.fab, name="snmp")
        ACISNMPClientGroup.objects.create(snmp_policy=pol, name="ops", mgmt_epg="oob")
        qs = ACISNMPClientGroupFilterSet({"q": "oob"}, queryset=ACISNMPClientGroup.objects.all()).qs
        self.assertEqual(qs.count(), 1)


class ACISNMPClientSearchTests(_Fixture):
    def test_address_match(self):
        pol = ACISNMPPolicy.objects.create(aci_fabric=self.fab, name="snmp")
        grp = ACISNMPClientGroup.objects.create(snmp_policy=pol, name="ops")
        ACISNMPClient.objects.create(client_group=grp, name="lan", address="10.0.0.0/24")
        qs = ACISNMPClientFilterSet({"q": "10.0.0"}, queryset=ACISNMPClient.objects.all()).qs
        self.assertEqual(qs.count(), 1)


class ACISNMPv3UserSearchTests(_Fixture):
    def test_name_match(self):
        pol = ACISNMPPolicy.objects.create(aci_fabric=self.fab, name="snmp")
        ACISNMPv3User.objects.create(snmp_policy=pol, name="netadmin")
        qs = ACISNMPv3UserFilterSet({"q": "netadmin"}, queryset=ACISNMPv3User.objects.all()).qs
        self.assertEqual(qs.count(), 1)


class ACISNMPTrapPolicySearchTests(_Fixture):
    def test_name_match(self):
        ACISNMPTrapPolicy.objects.create(aci_fabric=self.fab, name="traps")
        qs = ACISNMPTrapPolicyFilterSet({"q": "traps"}, queryset=ACISNMPTrapPolicy.objects.all()).qs
        self.assertEqual(qs.count(), 1)


class ACISNMPTrapDestSearchTests(_Fixture):
    def test_host_and_community_searchable(self):
        pol = ACISNMPTrapPolicy.objects.create(aci_fabric=self.fab, name="traps")
        ACISNMPTrapDest.objects.create(
            trap_policy=pol,
            name="d1",
            host="traps.example.com",
            community_or_user="alertmgr",
        )
        qs_host = ACISNMPTrapDestFilterSet(
            {"q": "traps.example"}, queryset=ACISNMPTrapDest.objects.all()
        ).qs
        qs_comm = ACISNMPTrapDestFilterSet(
            {"q": "alertmgr"}, queryset=ACISNMPTrapDest.objects.all()
        ).qs
        self.assertEqual(qs_host.count(), 1)
        self.assertEqual(qs_comm.count(), 1)


class ACIPodPolicyGroupSearchTests(_Fixture):
    def test_name_match(self):
        ACIPodPolicyGroup.objects.create(aci_fabric=self.fab, name="default-pg")
        qs = ACIPodPolicyGroupFilterSet(
            {"q": "default"}, queryset=ACIPodPolicyGroup.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)
