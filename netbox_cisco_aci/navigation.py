"""Top-level NetBox navigation entries for the plugin.

Navigation v0.2.0: reduced from 52 items to 19 across 6 groups.
v0.3.0: added a 7th group ("Pod Policies") with 5 items — total 24.
v0.4.0: added Pod Profile + the 3 new fabric-overlay control-plane
policies to the "Pod Policies" group — total now 28 items, 7 groups.

Child models (selectors, attachments, sub-entries, per-port policies,
all L3Out children, all pod-policy providers/destinations) are removed
from the sidebar but remain fully reachable via URL routes and parent
detail-page panels.
"""

from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem


def _item(link: str, text: str) -> PluginMenuItem:
    return PluginMenuItem(
        link=f"plugins:netbox_cisco_aci:{link}_list",
        link_text=text,
        buttons=(
            PluginMenuButton(
                link=f"plugins:netbox_cisco_aci:{link}_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    )


fabric_items = (
    _item("acifabric", "Fabrics"),
    _item("acipod", "Pods"),
    _item("acinode", "Nodes"),
)

tenancy_items = (
    _item("acitenant", "Tenants"),
    _item("acivrf", "VRFs"),
    _item("acibridgedomain", "Bridge Domains"),
    _item("aciappprofile", "Application Profiles"),
    _item("aciendpointgroup", "Endpoint Groups"),
    _item("aciendpointsecuritygroup", "Endpoint Security Groups"),
)

connectivity_items = (
    _item("aciaaep", "AAEPs"),
    _item("acidomain", "Domains"),
    _item("acivlanpool", "VLAN Pools"),
    _item("acistaticportbinding", "Static Port Bindings"),
)

contract_items = (
    _item("acicontract", "Contracts"),
    _item("acifilter", "Filters"),
)

l3out_items = (_item("acil3out", "L3Outs"),)

policy_items = (
    _item("aciinterfacepolicygroup", "Interface Policy Groups"),
    _item("aciswitchprofile", "Switch Profiles"),
    _item("aciinterfaceprofile", "Interface Profiles"),
)

# v0.3.0 — Pod policies. Parents only; child rows (providers,
# destinations, communities, client groups, clients, v3 users, trap
# destinations) reach via "Add" buttons on the parent's detail page,
# matching the convention established by Bundle A's nav cleanup.
pod_policy_items = (
    _item("acipodprofile", "Pod Profiles"),
    _item("acipodpolicygroup", "Pod Policy Groups"),
    _item("acintppolicy", "NTP Policies"),
    _item("acisyslogpolicy", "Syslog Policies"),
    _item("acisnmppolicy", "SNMP Policies"),
    _item("acisnmptrappolicy", "SNMP Trap Policies"),
    _item("acibgproutereflectorpolicy", "BGP RR Policies"),
    _item("acicoopgrouppolicy", "COOP Group Policies"),
    _item("aciisisdomainpolicy", "IS-IS Domain Policies"),
)

menu = PluginMenu(
    label="Cisco ACI",
    groups=(
        ("Fabric", fabric_items),
        ("Tenancy", tenancy_items),
        ("Connectivity", connectivity_items),
        ("Contracts", contract_items),
        ("L3Outs", l3out_items),
        ("Policies", policy_items),
        ("Pod Policies", pod_policy_items),
    ),
    icon_class="mdi mdi-server-network",
)
