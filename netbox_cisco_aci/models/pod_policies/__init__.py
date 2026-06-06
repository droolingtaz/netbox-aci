"""ACI Pod policies — NTP, Syslog, SNMP, SNMP Traps, BGP-RR, COOP, IS-IS,
Pod Profile + Pod Selector, and the Pod Policy Group that binds them.

These objects live at the *fabric* scope in APIC but may also be modeled
at the *tenant* scope when an operator wants per-tenant monitoring
overrides (e.g. a syslog forwarder that only fires for one tenant's
faults). All concrete policy models therefore carry a mandatory
``aci_fabric`` FK and an optional ``aci_tenant`` FK; leaving the tenant
unset means "fabric-wide".
"""

from .bgp_route_reflector import ACIBGPRouteReflectorNode, ACIBGPRouteReflectorPolicy
from .coop import ACICOOPGroupPolicy
from .isis import ACIISISDomainPolicy
from .ntp import ACINTPPolicy, ACINTPProvider
from .pod_policy_group import ACIPodPolicyGroup
from .pod_profile import ACIPodProfile, ACIPodSelector
from .snmp import (
    ACISNMPClient,
    ACISNMPClientGroup,
    ACISNMPCommunity,
    ACISNMPPolicy,
    ACISNMPv3User,
)
from .snmp_traps import ACISNMPTrapDest, ACISNMPTrapPolicy
from .syslog import ACISyslogPolicy, ACISyslogRemoteDest

__all__ = [
    "ACIBGPRouteReflectorNode",
    "ACIBGPRouteReflectorPolicy",
    "ACICOOPGroupPolicy",
    "ACIISISDomainPolicy",
    "ACINTPPolicy",
    "ACINTPProvider",
    "ACIPodPolicyGroup",
    "ACIPodProfile",
    "ACIPodSelector",
    "ACISNMPClient",
    "ACISNMPClientGroup",
    "ACISNMPCommunity",
    "ACISNMPPolicy",
    "ACISNMPTrapDest",
    "ACISNMPTrapPolicy",
    "ACISNMPv3User",
    "ACISyslogPolicy",
    "ACISyslogRemoteDest",
]
