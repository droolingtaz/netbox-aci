"""ACI Pod policies — NTP, Syslog, SNMP, SNMP Traps, and Pod Policy Group.

These objects live at the *fabric* scope in APIC but may also be modeled
at the *tenant* scope when an operator wants per-tenant monitoring
overrides (e.g. a syslog forwarder that only fires for one tenant's
faults). All concrete models therefore carry a mandatory ``aci_fabric``
FK and an optional ``aci_tenant`` FK; leaving the tenant unset means
"fabric-wide".
"""

from .ntp import ACINTPPolicy, ACINTPProvider
from .pod_policy_group import ACIPodPolicyGroup
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
    "ACINTPPolicy",
    "ACINTPProvider",
    "ACIPodPolicyGroup",
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
