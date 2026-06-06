"""UI views for the pod-policy family (NTP / Syslog / SNMP / SNMP Traps).

Reuses ``access._five_views`` so each of the twelve models gets the
standard list/edit/delete/bulk views without 400 lines of boilerplate.
"""

from ..filtersets.pod_policies import (
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
from ..forms.pod_policies import (
    ACINTPPolicyBulkEditForm,
    ACINTPPolicyFilterForm,
    ACINTPPolicyForm,
    ACINTPPolicyImportForm,
    ACINTPProviderBulkEditForm,
    ACINTPProviderFilterForm,
    ACINTPProviderForm,
    ACINTPProviderImportForm,
    ACIPodPolicyGroupBulkEditForm,
    ACIPodPolicyGroupFilterForm,
    ACIPodPolicyGroupForm,
    ACIPodPolicyGroupImportForm,
    ACISNMPClientBulkEditForm,
    ACISNMPClientFilterForm,
    ACISNMPClientForm,
    ACISNMPClientGroupBulkEditForm,
    ACISNMPClientGroupFilterForm,
    ACISNMPClientGroupForm,
    ACISNMPClientGroupImportForm,
    ACISNMPClientImportForm,
    ACISNMPCommunityBulkEditForm,
    ACISNMPCommunityFilterForm,
    ACISNMPCommunityForm,
    ACISNMPCommunityImportForm,
    ACISNMPPolicyBulkEditForm,
    ACISNMPPolicyFilterForm,
    ACISNMPPolicyForm,
    ACISNMPPolicyImportForm,
    ACISNMPTrapDestBulkEditForm,
    ACISNMPTrapDestFilterForm,
    ACISNMPTrapDestForm,
    ACISNMPTrapDestImportForm,
    ACISNMPTrapPolicyBulkEditForm,
    ACISNMPTrapPolicyFilterForm,
    ACISNMPTrapPolicyForm,
    ACISNMPTrapPolicyImportForm,
    ACISNMPv3UserBulkEditForm,
    ACISNMPv3UserFilterForm,
    ACISNMPv3UserForm,
    ACISNMPv3UserImportForm,
    ACISyslogPolicyBulkEditForm,
    ACISyslogPolicyFilterForm,
    ACISyslogPolicyForm,
    ACISyslogPolicyImportForm,
    ACISyslogRemoteDestBulkEditForm,
    ACISyslogRemoteDestFilterForm,
    ACISyslogRemoteDestForm,
    ACISyslogRemoteDestImportForm,
)
from ..models.pod_policies import (
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
from ..tables.pod_policies import (
    ACINTPPolicyTable,
    ACINTPProviderTable,
    ACIPodPolicyGroupTable,
    ACISNMPClientGroupTable,
    ACISNMPClientTable,
    ACISNMPCommunityTable,
    ACISNMPPolicyTable,
    ACISNMPTrapDestTable,
    ACISNMPTrapPolicyTable,
    ACISNMPv3UserTable,
    ACISyslogPolicyTable,
    ACISyslogRemoteDestTable,
)
from .access import _five_views


def _bind(views_dict, name):
    """Expose the dict produced by _five_views as module-level attrs."""
    globals()[f"{name}View"] = views_dict["view"]
    globals()[f"{name}ListView"] = views_dict["list"]
    globals()[f"{name}EditView"] = views_dict["edit"]
    globals()[f"{name}DeleteView"] = views_dict["delete"]
    globals()[f"{name}BulkImportView"] = views_dict["bulk_import"]
    globals()[f"{name}BulkEditView"] = views_dict["bulk_edit"]
    globals()[f"{name}BulkDeleteView"] = views_dict["bulk_delete"]


_bind(
    _five_views(
        ACINTPPolicy,
        ACINTPPolicyTable,
        ACINTPPolicyFilterSet,
        ACINTPPolicyFilterForm,
        ACINTPPolicyForm,
        ACINTPPolicyImportForm,
        ACINTPPolicyBulkEditForm,
        select=("aci_fabric", "aci_tenant"),
    ),
    "ACINTPPolicy",
)
_bind(
    _five_views(
        ACINTPProvider,
        ACINTPProviderTable,
        ACINTPProviderFilterSet,
        ACINTPProviderFilterForm,
        ACINTPProviderForm,
        ACINTPProviderImportForm,
        ACINTPProviderBulkEditForm,
        select=("ntp_policy",),
    ),
    "ACINTPProvider",
)
_bind(
    _five_views(
        ACISyslogPolicy,
        ACISyslogPolicyTable,
        ACISyslogPolicyFilterSet,
        ACISyslogPolicyFilterForm,
        ACISyslogPolicyForm,
        ACISyslogPolicyImportForm,
        ACISyslogPolicyBulkEditForm,
        select=("aci_fabric", "aci_tenant"),
    ),
    "ACISyslogPolicy",
)
_bind(
    _five_views(
        ACISyslogRemoteDest,
        ACISyslogRemoteDestTable,
        ACISyslogRemoteDestFilterSet,
        ACISyslogRemoteDestFilterForm,
        ACISyslogRemoteDestForm,
        ACISyslogRemoteDestImportForm,
        ACISyslogRemoteDestBulkEditForm,
        select=("syslog_policy",),
    ),
    "ACISyslogRemoteDest",
)
_bind(
    _five_views(
        ACISNMPPolicy,
        ACISNMPPolicyTable,
        ACISNMPPolicyFilterSet,
        ACISNMPPolicyFilterForm,
        ACISNMPPolicyForm,
        ACISNMPPolicyImportForm,
        ACISNMPPolicyBulkEditForm,
        select=("aci_fabric", "aci_tenant"),
    ),
    "ACISNMPPolicy",
)
_bind(
    _five_views(
        ACISNMPCommunity,
        ACISNMPCommunityTable,
        ACISNMPCommunityFilterSet,
        ACISNMPCommunityFilterForm,
        ACISNMPCommunityForm,
        ACISNMPCommunityImportForm,
        ACISNMPCommunityBulkEditForm,
        select=("snmp_policy",),
    ),
    "ACISNMPCommunity",
)
_bind(
    _five_views(
        ACISNMPClientGroup,
        ACISNMPClientGroupTable,
        ACISNMPClientGroupFilterSet,
        ACISNMPClientGroupFilterForm,
        ACISNMPClientGroupForm,
        ACISNMPClientGroupImportForm,
        ACISNMPClientGroupBulkEditForm,
        select=("snmp_policy",),
    ),
    "ACISNMPClientGroup",
)
_bind(
    _five_views(
        ACISNMPClient,
        ACISNMPClientTable,
        ACISNMPClientFilterSet,
        ACISNMPClientFilterForm,
        ACISNMPClientForm,
        ACISNMPClientImportForm,
        ACISNMPClientBulkEditForm,
        select=("client_group",),
    ),
    "ACISNMPClient",
)
_bind(
    _five_views(
        ACISNMPv3User,
        ACISNMPv3UserTable,
        ACISNMPv3UserFilterSet,
        ACISNMPv3UserFilterForm,
        ACISNMPv3UserForm,
        ACISNMPv3UserImportForm,
        ACISNMPv3UserBulkEditForm,
        select=("snmp_policy",),
    ),
    "ACISNMPv3User",
)
_bind(
    _five_views(
        ACISNMPTrapPolicy,
        ACISNMPTrapPolicyTable,
        ACISNMPTrapPolicyFilterSet,
        ACISNMPTrapPolicyFilterForm,
        ACISNMPTrapPolicyForm,
        ACISNMPTrapPolicyImportForm,
        ACISNMPTrapPolicyBulkEditForm,
        select=("aci_fabric", "aci_tenant"),
    ),
    "ACISNMPTrapPolicy",
)
_bind(
    _five_views(
        ACISNMPTrapDest,
        ACISNMPTrapDestTable,
        ACISNMPTrapDestFilterSet,
        ACISNMPTrapDestFilterForm,
        ACISNMPTrapDestForm,
        ACISNMPTrapDestImportForm,
        ACISNMPTrapDestBulkEditForm,
        select=("trap_policy",),
    ),
    "ACISNMPTrapDest",
)
_bind(
    _five_views(
        ACIPodPolicyGroup,
        ACIPodPolicyGroupTable,
        ACIPodPolicyGroupFilterSet,
        ACIPodPolicyGroupFilterForm,
        ACIPodPolicyGroupForm,
        ACIPodPolicyGroupImportForm,
        ACIPodPolicyGroupBulkEditForm,
        select=(
            "aci_fabric",
            "ntp_policy",
            "syslog_policy",
            "snmp_policy",
            "snmp_trap_policy",
        ),
    ),
    "ACIPodPolicyGroup",
)
