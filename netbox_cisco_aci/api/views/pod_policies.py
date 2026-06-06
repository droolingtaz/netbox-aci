"""DRF ViewSets for the pod-policy family."""

from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.pod_policies import (
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
from ...models.pod_policies import (
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
from ..serializers.pod_policies import (
    ACINTPPolicySerializer,
    ACINTPProviderSerializer,
    ACIPodPolicyGroupSerializer,
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
    )
    serializer_class = ACIPodPolicyGroupSerializer
    filterset_class = ACIPodPolicyGroupFilterSet
