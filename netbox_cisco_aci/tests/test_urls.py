"""URL resolution sanity tests.

These exist because NetBox 4.x detail and list-row templates reverse
``<label>_changelog`` and ``<label>_journal`` unconditionally. A plugin
that registers the basic CRUD verbs but forgets the changelog / journal
routes (as we did for the very first cut of the plugin's URL patterns)
will silently pass ``NetBoxModelViewTestCase.*`` because those test
classes only reverse the explicit verbs they cover. The user only
discovers the gap when they click on a list page in a real browser
and gets a 500-error page from ``django.urls.exceptions.NoReverseMatch``.

The tests below close that loop: every model in the plugin must expose
the full ten-route block (list / add / import / bulk-edit / bulk-delete /
detail / edit / delete / **changelog** / **journal**) and each route
must resolve cleanly.
"""

from django.test import TestCase
from django.urls import NoReverseMatch, reverse

# Every UI-bearing model in the plugin, identified by the label passed
# to ``_crud(...)`` in netbox_cisco_aci/urls.py. When a new model is
# added, the entry must be added here too — this list is the simplest
# regression guard we have for "a brand-new model wires up its CRUD
# routes but forgets changelog/journal".
PLUGIN_MODELS = [
    # Phase 1 — Fabric
    "acifabric",
    "acipod",
    "acinode",
    # Phase 2 — Tenancy
    "acitenant",
    "acivrf",
    "acibridgedomain",
    "acibridgedomainsubnet",
    "aciappprofile",
    "aciendpointgroup",
    "aciusegattribute",
    "aciendpointsecuritygroup",
    # Phase 3 — Access Phase A
    "acivlanpool",
    "acivlanpoolblock",
    "acidomain",
    "aciaaep",
    "aciaaepepgmapping",
    # Phase 4 — Access Phase B
    "acilinklevelpolicy",
    "acicdpinterfacepolicy",
    "acilldpinterfacepolicy",
    "acilacpinterfacepolicy",
    "acimcpinterfacepolicy",
    "acistpinterfacepolicy",
    "aciinterfacepolicygroup",
    "aciswitchprofile",
    "aciswitchprofileselector",
    "aciinterfaceprofile",
    "aciinterfaceprofileselector",
    "aciswitchprofileinterfaceprofileattachment",
    # Phase 5 — Contracts
    "acicontract",
    "acisubject",
    "acifilter",
    "acifilterentry",
    "acisubjectfilter",
    "acicontractrelation",
    # Phase 6 — Bindings
    "acistaticportbinding",
    "acivpcbindingpair",
    "acidomainbinding",
    "aciinterfacefabricmembership",
    # Phase 7 — L3Outs
    "acil3out",
    "acilogicalnodeprofile",
    "acilogicalnode",
    "acilogicalinterfaceprofile",
    "acil3outinterface",
    "acibgppeer",
    "aciospfinterfacepolicy",
    "aciospfinterfaceattachment",
    "acieigrpinterfacepolicy",
    "aciexternalepg",
    "aciexternalepgsubnet",
    # Phase 7.1 — Static routes
    "acil3outstaticroute",
    "acil3outstaticroutenexthop",
    # v0.2.0 — BFD
    "acibfdinterfacepolicy",
    "acibfdinterfaceattachment",
    # v0.3.0 — Pod policies
    "acipodpolicygroup",
    "acintppolicy",
    "acintpprovider",
    "acisyslogpolicy",
    "acisyslogremotedest",
    "acisnmppolicy",
    "acisnmpcommunity",
    "acisnmpclientgroup",
    "acisnmpclient",
    "acisnmpv3user",
    "acisnmptrappolicy",
    "acisnmptrapdest",
]


class PluginURLPatternsTests(TestCase):
    """Every model's ten standard routes must resolve."""

    # The five routes that don't take a pk argument.
    PK_LESS = ["list", "add", "import", "bulk_edit", "bulk_delete"]

    # The five routes that take a single pk argument.
    PK_BOUND = ["", "edit", "delete", "changelog", "journal"]

    def _name(self, label, suffix):
        return f"plugins:netbox_cisco_aci:{label}{('_' + suffix) if suffix else ''}"

    def test_all_models_expose_pk_less_routes(self):
        for label in PLUGIN_MODELS:
            for suffix in self.PK_LESS:
                with self.subTest(label=label, suffix=suffix):
                    try:
                        reverse(self._name(label, suffix))
                    except NoReverseMatch as exc:
                        self.fail(f"reverse() failed for {label}_{suffix}: {exc}")

    def test_all_models_expose_pk_bound_routes(self):
        for label in PLUGIN_MODELS:
            for suffix in self.PK_BOUND:
                with self.subTest(label=label, suffix=suffix):
                    try:
                        reverse(self._name(label, suffix), kwargs={"pk": 1})
                    except NoReverseMatch as exc:
                        self.fail(f"reverse() failed for {label}_{suffix}: {exc}")

    def test_changelog_and_journal_routes_resolve(self):
        """Explicit, dedicated coverage for the routes that triggered
        the original 500 the user hit: the production crash was
        ``Reverse for 'acifabric_changelog' not found``, so we want a
        named test that fails loudly if those two routes ever
        regress."""
        for label in PLUGIN_MODELS:
            for suffix in ("changelog", "journal"):
                with self.subTest(label=label, suffix=suffix):
                    url = reverse(self._name(label, suffix), kwargs={"pk": 1})
                    self.assertTrue(
                        url.endswith(f"/{suffix}/"),
                        f"{label}_{suffix} resolved to {url!r} which does not end with /{suffix}/",
                    )


class NavigationStructureTests(TestCase):
    """Verify the 24-item, 7-group navigation shape is intact.

    v0.2.0 reduced the menu from 52 items to 19 across 6 groups.
    v0.3.0 added a 7th group ("Pod Policies") with 5 items — total 24.
    """

    def test_menu_has_seven_groups(self):
        from netbox_cisco_aci.navigation import menu

        self.assertEqual(len(menu.groups), 7)

    def test_menu_has_expected_items(self):
        from netbox_cisco_aci.navigation import menu

        total = sum(len(g.items) for g in menu.groups)
        self.assertEqual(total, 24)  # 3+6+4+2+1+3+5

    def test_group_item_counts(self):
        from netbox_cisco_aci.navigation import menu

        groups = {g.label: g.items for g in menu.groups}
        self.assertEqual(len(groups["Fabric"]), 3)
        self.assertEqual(len(groups["Tenancy"]), 6)
        self.assertEqual(len(groups["Connectivity"]), 4)
        self.assertEqual(len(groups["Contracts"]), 2)
        self.assertEqual(len(groups["L3Outs"]), 1)
        self.assertEqual(len(groups["Policies"]), 3)
        self.assertEqual(len(groups["Pod Policies"]), 5)

    def test_all_menu_urls_resolve(self):
        from netbox_cisco_aci.navigation import menu

        for g in menu.groups:
            for item in g.items:
                with self.subTest(link=item.link):
                    try:
                        reverse(item.link)
                    except NoReverseMatch as exc:
                        self.fail(f"Menu item {item.link} failed to resolve: {exc}")
