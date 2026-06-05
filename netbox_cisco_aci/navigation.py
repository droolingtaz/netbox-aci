"""Top-level NetBox navigation entries for the plugin.

Navigation v0.2.0: reduced from 52 items to 17.
Child models (selectors, attachments, sub-entries, per-port policies,
all L3Out children) are removed from the sidebar but remain fully
reachable via URL routes and parent detail-page panels.
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

menu = PluginMenu(
    label="Cisco ACI",
    groups=(
        ("Fabric", fabric_items),
        ("Tenancy", tenancy_items),
        ("Connectivity", connectivity_items),
        ("Contracts", contract_items),
        ("L3Outs", l3out_items),
        ("Policies", policy_items),
    ),
    icon_class="mdi mdi-server-network",
)
