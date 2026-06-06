"""SearchIndex registrations for the global NetBox search."""

from netbox.search import SearchIndex, register_search

from .models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACICDPInterfacePolicy,
    ACIDomain,
    ACIInterfacePolicyGroup,
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from .models.bindings import (
    ACIDomainBinding,
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
    ACIVPCBindingPair,
)
from .models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from .models.fabric import ACIFabric, ACINode, ACIPod
from .models.l3out import (
    ACIBFDInterfaceAttachment,
    ACIBFDInterfacePolicy,
    ACIBGPPeer,
    ACIEIGRPInterfacePolicy,
    ACIExternalEPG,
    ACIExternalEPGSubnet,
    ACIL3Out,
    ACIL3OutInterface,
    ACIL3OutStaticRoute,
    ACIL3OutStaticRouteNextHop,
    ACILogicalInterfaceProfile,
    ACILogicalNode,
    ACILogicalNodeProfile,
    ACIOSPFInterfaceAttachment,
    ACIOSPFInterfacePolicy,
)
from .models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
)


@register_search
class ACIFabricIndex(SearchIndex):
    model = ACIFabric
    fields = (("name", 100), ("description", 500), ("fabric_id", 100))


@register_search
class ACIPodIndex(SearchIndex):
    model = ACIPod
    fields = (("name", 100), ("description", 500), ("pod_id", 100))


@register_search
class ACINodeIndex(SearchIndex):
    model = ACINode
    fields = (
        ("name", 100),
        ("description", 500),
        ("node_id", 100),
        ("serial_number", 200),
    )


@register_search
class ACITenantIndex(SearchIndex):
    model = ACITenant
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIVRFIndex(SearchIndex):
    model = ACIVRF
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIBridgeDomainIndex(SearchIndex):
    model = ACIBridgeDomain
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIBridgeDomainSubnetIndex(SearchIndex):
    model = ACIBridgeDomainSubnet
    fields = (("gateway_ip", 100), ("name", 200), ("description", 500))


@register_search
class ACIAppProfileIndex(SearchIndex):
    model = ACIAppProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIEndpointGroupIndex(SearchIndex):
    model = ACIEndpointGroup
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIUSegAttributeIndex(SearchIndex):
    model = ACIUSegAttribute
    fields = (("name", 100), ("match_value", 200), ("description", 500))


@register_search
class ACIEndpointSecurityGroupIndex(SearchIndex):
    model = ACIEndpointSecurityGroup
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIVLANPoolIndex(SearchIndex):
    model = ACIVLANPool
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIVLANPoolBlockIndex(SearchIndex):
    model = ACIVLANPoolBlock
    fields = (("name", 100), ("description", 500))


@register_search
class ACIDomainIndex(SearchIndex):
    model = ACIDomain
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIAAEPIndex(SearchIndex):
    model = ACIAAEP
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIAAEPEPGMappingIndex(SearchIndex):
    model = ACIAAEPEPGMapping
    fields = (("name", 100), ("description", 500))


# Phase 4 — Interface policies, policy groups, profiles


@register_search
class ACILinkLevelPolicyIndex(SearchIndex):
    model = ACILinkLevelPolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACICDPInterfacePolicyIndex(SearchIndex):
    model = ACICDPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACILLDPInterfacePolicyIndex(SearchIndex):
    model = ACILLDPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACILACPInterfacePolicyIndex(SearchIndex):
    model = ACILACPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIMCPInterfacePolicyIndex(SearchIndex):
    model = ACIMCPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISTPInterfacePolicyIndex(SearchIndex):
    model = ACISTPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIInterfacePolicyGroupIndex(SearchIndex):
    model = ACIInterfacePolicyGroup
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISwitchProfileIndex(SearchIndex):
    model = ACISwitchProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISwitchProfileSelectorIndex(SearchIndex):
    model = ACISwitchProfileSelector
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIInterfaceProfileIndex(SearchIndex):
    model = ACIInterfaceProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIInterfaceProfileSelectorIndex(SearchIndex):
    model = ACIInterfaceProfileSelector
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISwitchProfileInterfaceProfileAttachmentIndex(SearchIndex):
    model = ACISwitchProfileInterfaceProfileAttachment
    fields = ()


# Phase 5 — Contracts / Subjects / Filters / Relations


@register_search
class ACIContractIndex(SearchIndex):
    model = ACIContract
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISubjectIndex(SearchIndex):
    model = ACISubject
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIFilterIndex(SearchIndex):
    model = ACIFilter
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIFilterEntryIndex(SearchIndex):
    model = ACIFilterEntry
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISubjectFilterIndex(SearchIndex):
    model = ACISubjectFilter
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIContractRelationIndex(SearchIndex):
    model = ACIContractRelation
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


# Phase 6 — Static Port Bindings


@register_search
class ACIStaticPortBindingIndex(SearchIndex):
    model = ACIStaticPortBinding
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIVPCBindingPairIndex(SearchIndex):
    model = ACIVPCBindingPair
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIDomainBindingIndex(SearchIndex):
    model = ACIDomainBinding
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIInterfaceFabricMembershipIndex(SearchIndex):
    model = ACIInterfaceFabricMembership
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


# Phase 7 — L3Outs


@register_search
class ACIBFDInterfacePolicyIndex(SearchIndex):
    model = ACIBFDInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIBFDInterfaceAttachmentIndex(SearchIndex):
    model = ACIBFDInterfaceAttachment
    fields = (("name", 100), ("description", 500))


@register_search
class ACIL3OutIndex(SearchIndex):
    model = ACIL3Out
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACILogicalNodeProfileIndex(SearchIndex):
    model = ACILogicalNodeProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACILogicalNodeIndex(SearchIndex):
    model = ACILogicalNode
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACILogicalInterfaceProfileIndex(SearchIndex):
    model = ACILogicalInterfaceProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIL3OutInterfaceIndex(SearchIndex):
    model = ACIL3OutInterface
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIBGPPeerIndex(SearchIndex):
    model = ACIBGPPeer
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIOSPFInterfacePolicyIndex(SearchIndex):
    model = ACIOSPFInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIOSPFInterfaceAttachmentIndex(SearchIndex):
    model = ACIOSPFInterfaceAttachment
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIEIGRPInterfacePolicyIndex(SearchIndex):
    model = ACIEIGRPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIExternalEPGIndex(SearchIndex):
    model = ACIExternalEPG
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIExternalEPGSubnetIndex(SearchIndex):
    model = ACIExternalEPGSubnet
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIL3OutStaticRouteIndex(SearchIndex):
    model = ACIL3OutStaticRoute
    fields = (
        ("name", 100),
        ("name_alias", 200),
        ("prefix", 100),
        ("description", 500),
    )


@register_search
class ACIL3OutStaticRouteNextHopIndex(SearchIndex):
    model = ACIL3OutStaticRouteNextHop
    fields = (
        ("name", 100),
        ("name_alias", 200),
        ("nexthop_address", 100),
        ("description", 500),
    )


# ---------------------------------------------------------------------------
# v0.3.0 — Pod policies
# ---------------------------------------------------------------------------

from .models.pod_policies import (  # noqa: E402
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


@register_search
class ACINTPPolicyIndex(SearchIndex):
    model = ACINTPPolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACINTPProviderIndex(SearchIndex):
    model = ACINTPProvider
    fields = (("host", 100), ("name", 200), ("description", 500))


@register_search
class ACISyslogPolicyIndex(SearchIndex):
    model = ACISyslogPolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISyslogRemoteDestIndex(SearchIndex):
    model = ACISyslogRemoteDest
    fields = (("host", 100), ("name", 200), ("description", 500))


@register_search
class ACISNMPPolicyIndex(SearchIndex):
    model = ACISNMPPolicy
    fields = (
        ("name", 100),
        ("name_alias", 200),
        ("contact", 300),
        ("location", 300),
        ("description", 500),
    )


@register_search
class ACISNMPCommunityIndex(SearchIndex):
    model = ACISNMPCommunity
    fields = (("name", 100), ("description", 500))


@register_search
class ACISNMPClientGroupIndex(SearchIndex):
    model = ACISNMPClientGroup
    fields = (("name", 100), ("mgmt_epg", 300), ("description", 500))


@register_search
class ACISNMPClientIndex(SearchIndex):
    model = ACISNMPClient
    fields = (("address", 100), ("name", 200), ("description", 500))


@register_search
class ACISNMPv3UserIndex(SearchIndex):
    model = ACISNMPv3User
    fields = (("name", 100), ("description", 500))


@register_search
class ACISNMPTrapPolicyIndex(SearchIndex):
    model = ACISNMPTrapPolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISNMPTrapDestIndex(SearchIndex):
    model = ACISNMPTrapDest
    fields = (
        ("host", 100),
        ("community_or_user", 200),
        ("name", 300),
        ("description", 500),
    )


@register_search
class ACIPodPolicyGroupIndex(SearchIndex):
    model = ACIPodPolicyGroup
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


# ---------------------------------------------------------------------------
# v0.4.0 — Pod Profile + extended fabric-overlay bindings
# ---------------------------------------------------------------------------

from .models.pod_policies import (  # noqa: E402
    ACIBGPRouteReflectorNode,
    ACIBGPRouteReflectorPolicy,
    ACICOOPGroupPolicy,
    ACIISISDomainPolicy,
    ACIPodProfile,
    ACIPodSelector,
)


@register_search
class ACIBGPRouteReflectorPolicyIndex(SearchIndex):
    model = ACIBGPRouteReflectorPolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIBGPRouteReflectorNodeIndex(SearchIndex):
    model = ACIBGPRouteReflectorNode
    fields = (("name", 100), ("description", 500))


@register_search
class ACICOOPGroupPolicyIndex(SearchIndex):
    model = ACICOOPGroupPolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIISISDomainPolicyIndex(SearchIndex):
    model = ACIISISDomainPolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIPodProfileIndex(SearchIndex):
    model = ACIPodProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIPodSelectorIndex(SearchIndex):
    model = ACIPodSelector
    fields = (("name", 100), ("name_alias", 200), ("description", 500))
