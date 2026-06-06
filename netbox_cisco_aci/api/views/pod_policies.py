"""DRF ViewSets for the pod-policy family."""

from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.pod_policies import (
    ACIBGPRouteReflectorNodeFilterSet,
    ACIBGPRouteReflectorPolicyFilterSet,
    ACICOOPGroupPolicyFilterSet,
    ACIISISDomainPolicyFilterSet,
    ACINTPPolicyFilterSet,
    ACINTPProviderFilterSet,
    ACIPodPolicyGroupFilterSet,
    ACIPodProfileFilterSet,
    ACIPodSelectorFilterSet,
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
from ...models.pod_policies import (
    ACIBGPRouteReflectorNode,
    ACIBGPRouteReflectorPolicy,
    ACICOOPGroupPolicy,
    ACIISISDomainPolicy,
    ACINTPPolicy,
    ACINTPProvider,
    ACIPodPolicyGroup,
    ACIPodProfile,
    ACIPodSelector,
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
from ..serializers.pod_policies import (
    ACIBGPRouteReflectorNodeSerializer,
    ACIBGPRouteReflectorPolicySerializer,
    ACICOOPGroupPolicySerializer,
    ACIISISDomainPolicySerializer,
    ACINTPPolicySerializer,
    ACINTPProviderSerializer,
    ACIPodPolicyGroupSerializer,
    ACIPodProfileSerializer,
    ACIPodSelectorSerializer,
    ACISNMPClientGroupSerializer,
    ACISNMPClientSerializer,
    ACISNMPCommunitySerializer,
    ACISNMPPolicySerializer,
    ACISNMPTrapDestSerializer,
    ACISNMPTrapPolicySerializer,
    ACISNMPv3UserSerializer,
    ACISyslogPolicySerializer,
    ACISyslogRemoteDestSerializer,
)


class ACINTPPolicyViewSet(NetBoxModelViewSet):
    queryset = ACINTPPolicy.objects.select_related("aci_fabric", "aci_tenant")
    serializer_class = ACINTPPolicySerializer
    filterset_class = ACINTPPolicyFilterSet


class ACINTPProviderViewSet(NetBoxModelViewSet):
    queryset = ACINTPProvider.objects.select_related("ntp_policy")
    serializer_class = ACINTPProviderSerializer
    filterset_class = ACINTPProviderFilterSet


class ACISyslogPolicyViewSet(NetBoxModelViewSet):
    queryset = ACISyslogPolicy.objects.select_related("aci_fabric", "aci_tenant")
    serializer_class = ACISyslogPolicySerializer
    filterset_class = ACISyslogPolicyFilterSet


class ACISyslogRemoteDestViewSet(NetBoxModelViewSet):
    queryset = ACISyslogRemoteDest.objects.select_related("syslog_policy")
    serializer_class = ACISyslogRemoteDestSerializer
    filterset_class = ACISyslogRemoteDestFilterSet


class ACISNMPPolicyViewSet(NetBoxModelViewSet):
    queryset = ACISNMPPolicy.objects.select_related("aci_fabric", "aci_tenant")
    serializer_class = ACISNMPPolicySerializer
    filterset_class = ACISNMPPolicyFilterSet


class ACISNMPCommunityViewSet(NetBoxModelViewSet):
    queryset = ACISNMPCommunity.objects.select_related("snmp_policy")
    serializer_class = ACISNMPCommunitySerializer
    filterset_class = ACISNMPCommunityFilterSet


class ACISNMPClientGroupViewSet(NetBoxModelViewSet):
    queryset = ACISNMPClientGroup.objects.select_related("snmp_policy")
    serializer_class = ACISNMPClientGroupSerializer
    filterset_class = ACISNMPClientGroupFilterSet


class ACISNMPClientViewSet(NetBoxModelViewSet):
    queryset = ACISNMPClient.objects.select_related("client_group")
    serializer_class = ACISNMPClientSerializer
    filterset_class = ACISNMPClientFilterSet


class ACISNMPv3UserViewSet(NetBoxModelViewSet):
    queryset = ACISNMPv3User.objects.select_related("snmp_policy")
    serializer_class = ACISNMPv3UserSerializer
    filterset_class = ACISNMPv3UserFilterSet


class ACISNMPTrapPolicyViewSet(NetBoxModelViewSet):
    queryset = ACISNMPTrapPolicy.objects.select_related("aci_fabric", "aci_tenant")
    serializer_class = ACISNMPTrapPolicySerializer
    filterset_class = ACISNMPTrapPolicyFilterSet


class ACISNMPTrapDestViewSet(NetBoxModelViewSet):
    queryset = ACISNMPTrapDest.objects.select_related("trap_policy")
    serializer_class = ACISNMPTrapDestSerializer
    filterset_class = ACISNMPTrapDestFilterSet


class ACIPodPolicyGroupViewSet(NetBoxModelViewSet):
    queryset = ACIPodPolicyGroup.objects.select_related(
        "aci_fabric",
        "ntp_policy",
        "syslog_policy",
        "snmp_policy",
        "snmp_trap_policy",
        "bgp_rr_policy",
        "coop_policy",
        "isis_policy",
        "datetime_policy",
    )
    serializer_class = ACIPodPolicyGroupSerializer
    filterset_class = ACIPodPolicyGroupFilterSet


class ACIBGPRouteReflectorPolicyViewSet(NetBoxModelViewSet):
    queryset = ACIBGPRouteReflectorPolicy.objects.select_related("aci_fabric", "aci_tenant")
    serializer_class = ACIBGPRouteReflectorPolicySerializer
    filterset_class = ACIBGPRouteReflectorPolicyFilterSet


class ACIBGPRouteReflectorNodeViewSet(NetBoxModelViewSet):
    queryset = ACIBGPRouteReflectorNode.objects.select_related("bgp_rr_policy")
    serializer_class = ACIBGPRouteReflectorNodeSerializer
    filterset_class = ACIBGPRouteReflectorNodeFilterSet


class ACICOOPGroupPolicyViewSet(NetBoxModelViewSet):
    queryset = ACICOOPGroupPolicy.objects.select_related("aci_fabric", "aci_tenant")
    serializer_class = ACICOOPGroupPolicySerializer
    filterset_class = ACICOOPGroupPolicyFilterSet


class ACIISISDomainPolicyViewSet(NetBoxModelViewSet):
    queryset = ACIISISDomainPolicy.objects.select_related("aci_fabric", "aci_tenant")
    serializer_class = ACIISISDomainPolicySerializer
    filterset_class = ACIISISDomainPolicyFilterSet


class ACIPodProfileViewSet(NetBoxModelViewSet):
    queryset = ACIPodProfile.objects.select_related("aci_fabric")
    serializer_class = ACIPodProfileSerializer
    filterset_class = ACIPodProfileFilterSet


class ACIPodSelectorViewSet(NetBoxModelViewSet):
    queryset = ACIPodSelector.objects.select_related("pod_profile", "pod_policy_group")
    serializer_class = ACIPodSelectorSerializer
    filterset_class = ACIPodSelectorFilterSet
