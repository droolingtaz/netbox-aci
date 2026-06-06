# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [0.4.0] — 2026-06-06

Fills out the fabric-overlay control-plane policies that APIC's
pod-policy-group actually contains, and adds the **Pod Profile / Pod
Selector** binding layer that applies a pod-policy-group to a pod.

> **Compatibility:** NetBox v4.6 only · Python 3.12.

### Added

- **Pod Profile family** (PR #28). New `ACIPodProfile` (`fabricPodP`)
  + `ACIPodSelector` (`fabricPodS`). A selector is range/ALL and
  points at exactly one `ACIPodPolicyGroup`; `clean()` enforces the
  range/ALL invariants and `pod_block_from <= pod_block_to`.
- **BGP Route Reflector policy** — `ACIBGPRouteReflectorPolicy`
  (`bgpRRP`) holds the overlay ASN; child `ACIBGPRouteReflectorNode`
  (`bgpRRNodePEp`) pins which spine node IDs act as route reflectors.
- **COOP Group policy** — `ACICOOPGroupPolicy` (`coopPol`) exposes
  the strict/compatible MD5 authentication knob between spines.
- **IS-IS Domain policy** — `ACIISISDomainPolicy` (`isisDomPol`) covers
  metric style + LSP timers + fast-flood for the underlay.
- **Four new optional FK slots on `ACIPodPolicyGroup`**, all `SET_NULL`:
  - `bgp_rr_policy` → `ACIBGPRouteReflectorPolicy`
  - `coop_policy` → `ACICOOPGroupPolicy`
  - `isis_policy` → `ACIISISDomainPolicy`
  - `datetime_policy` → `ACINTPPolicy` (APIC's `datetimePol` MO is
    structurally the same object as an NTP policy, so we reuse rather
    than create a duplicate `ACIDateTimePolicy` model).
- **Choices**: `COOPAuthenticationTypeChoices`, `ISISMetricStyleChoices`.
- **API**: 7 new endpoints — `bgp-rr-policies`, `bgp-rr-nodes`,
  `coop-policies`, `isis-policies`, `pod-profiles`, `pod-selectors`,
  plus the existing `pod-policy-groups` endpoint serializing the 4
  new slots.
- **Migration `0013_pod_profile_and_bindings`** adds 7 new tables,
  4 new FK columns on `acipodpolicygroup`, and 12 partial unique
  constraints.

### Changed

- **Navigation: "Pod Policies" group grows from 5 to 9 items**
  (added Pod Profiles, BGP RR Policies, COOP Group Policies, IS-IS
  Domain Policies). Total menu now **28 items / 7 groups**.
- `ACIPodPolicyGroupForm` / table / filterset / detail template all
  gain surfaces for the four new FK slots.

### Notes

- The user asked us to audit whether `snmp_trap_policy` was visible
  on the pod-policy-group UI. Confirmed it was already wired through
  the form, table, and detail template since v0.3.0 — no fix needed.
- Spine node IDs on `ACIBGPRouteReflectorNode` are stored as plain
  integers rather than FKs to `ACINode`, so APIC's accept-then-create
  flow continues to work even if the matching `ACINode` row hasn't
  been imported yet.

---

## [0.3.0] — 2026-06-06

This release adds the operational pod-policy family the plugin was
missing: NTP, Syslog, SNMP, and SNMP traps, plus the Pod Policy Group
that actually binds them to a pod in APIC. Everything new lives under
the new top-level "Pod Policies" menu group.

> **Compatibility:** NetBox v4.6 only · Python 3.12.

### Added

- **Pod Policies family** (PR #26). Twelve new models grouped under a
  new top-level menu "Pod Policies":
  - `ACINTPPolicy` + `ACINTPProvider` (maps `datetimeNtpPol` /
    `datetimeNtpProv`).
  - `ACISyslogPolicy` + `ACISyslogRemoteDest` (maps `syslogGroup` /
    `syslogRemoteDest`).
  - `ACISNMPPolicy` + `ACISNMPCommunity`, `ACISNMPClientGroup` →
    `ACISNMPClient`, `ACISNMPv3User` (maps `snmpPol` and its
    children).
  - `ACISNMPTrapPolicy` + `ACISNMPTrapDest` (maps `snmpTrapFwdServerP`
    group).
  - `ACIPodPolicyGroup` — binds NTP / Syslog / SNMP / SNMP-Trap
    policies together (maps `fabricPodPGrp`).
  - Migration `0012_pod_policies` adds all twelve tables plus 16
    constraints (8 fabric/tenant partial uniques, 8 child uniques,
    plus the partial unique enforcing "at most one preferred provider
    per NTP policy").
- **Fabric-scoped with optional tenant override.** Every policy parent
  carries `aci_fabric` (mandatory) and `aci_tenant` (optional). Two
  partial `UniqueConstraint`s per policy (one for `aci_tenant IS NULL`,
  one for `aci_tenant IS NOT NULL`) enforce per-scope uniqueness without
  tripping on PostgreSQL's NULL-distinct default.
- **Validations.**
  - `ACINTPProvider`: `min_poll <= max_poll`.
  - `ACINTPProvider`: at most one row per policy with `role='preferred'`.
  - `ACISNMPTrapDest`: `v3_security_level` only meaningful when
    `version=v3`.
- **API**: twelve new endpoints under `/api/plugins/aci/` —
  `ntp-policies`, `ntp-providers`, `syslog-policies`,
  `syslog-remote-destinations`, `snmp-policies`, `snmp-communities`,
  `snmp-client-groups`, `snmp-clients`, `snmp-v3-users`,
  `snmp-trap-policies`, `snmp-trap-destinations`, `pod-policy-groups`.
- **Choices**: `NTPProviderStateChoices`, `SyslogSeverityChoices`,
  `SyslogFacilityChoices`, `SNMPAuthProtocolChoices`,
  `SNMPPrivProtocolChoices`, `SNMPSecurityLevelChoices`,
  `SNMPVersionChoices`. The pre-existing `EnabledDisabledChoices`
  is reused for every `admin_state` column.

### Changed

- **Navigation: 19 items / 6 groups → 24 items / 7 groups.** New
  "Pod Policies" group exposes the five parents (Pod Policy Groups,
  NTP Policies, Syslog Policies, SNMP Policies, SNMP Trap Policies).
  Children reach via parent-detail "Add" buttons, same convention
  established by Bundle A in v0.2.0.

### Notes

- Server host fields (`ACINTPProvider.host`,
  `ACISyslogRemoteDest.host`, `ACISNMPTrapDest.host`, `ACISNMPClient.address`)
  are free-form `CharField`s rather than IPAM-linked. NTP/syslog/SNMP
  servers are routinely referenced by FQDN, and APIC accepts either,
  so this mirrors APIC's free-form input. A future minor can layer on
  Bundle B's deprecation-friendly IPAM linkage if any of these need to
  participate in IPAM utilisation reporting.
- SNMPv3 user records do not store auth/privacy secrets — secrets live
  on APIC. The plugin tracks the user record for operational visibility
  (which user belongs to which policy) and surfaces a note on the
  detail page reminding operators to rotate secrets out-of-band.

---

## [0.2.0] — 2026-06-05

First minor release on the NetBox 4.6 line. Two themes: tighten the
UX and validation guarantees on top of NetBox 4.6, and start treating
the ACI BD gateway as a first-class NetBox IPAM citizen.

> **Compatibility:** NetBox v4.6 only (4.5 support dropped) · Python 3.12.

### Added

- **BFD policy + attachment models.** `ACIBFDInterfacePolicy` and
  `ACIBFDInterfaceAttachment` cover BFD on L3Out logical interfaces
  (migration `0010_bfd`), with the same model/form/serializer/table/
  filterset shape as the rest of the L3Out hierarchy.
- **BD Subnet IPAM linkage** (PR #24). New
  `ACIBridgeDomainSubnet.gateway_ipam_ip_address` ForeignKey →
  `ipam.IPAddress` (nullable, `SET_NULL`). The new field is the
  preferred representation; it participates in NetBox search, IPAM
  utilisation, and audit reporting. Both representations stay visible
  during the deprecation window, and a new `display_gateway` property
  picks IPAM over the legacy string for `__str__`, templates, and the
  filterset `q` search. Per-BD uniqueness is preserved on each
  representation via two partial `UniqueConstraint`s
  (`netbox_cisco_aci_acibdsubnet_bd_gw_unique`,
  `netbox_cisco_aci_acibdsubnet_bd_ipam_unique`). `clean()` requires
  at least one of the two representations to be set. Migration
  `0011_bridgedomainsubnet_ipam_ip_address` adds the field, drops the
  pre-existing non-partial unique, and installs the two partial
  uniques.
- **`PLUGINS_CONFIG['netbox_cisco_aci']['l3out_default_protocols']`**
  to seed L3Out protocol checkboxes on the create form at site level.
- **New validations.**
  - **EPG static port binding**: `encap_vlan` must fall within a VLAN
    pool block reachable through the EPG's domain bindings.
  - **External EPG subnet**: prefix must be unique across all L3Outs
    sharing the same VRF.
  - **AAEP domain association**: cannot attach two domains whose VLAN
    pool blocks overlap.
- **"Add" buttons** on parent detail-page panels for every child model
  removed from the sidebar.

### Changed

- **BREAKING**: NetBox 4.6 only. NetBox 4.5 support is dropped.
  `min_version = max_version = "4.6.x"`. CI matrix narrowed to a
  single `v4.6.0` entry.
- **BREAKING (UI)**: Navigation cleaned up from 52 menu items to 19
  across 6 groups (Fabric, Tenancy, Connectivity, Contracts, L3Outs,
  Policies). Child models (selectors, attachments, sub-entries,
  per-port policies, every L3Out child) are removed from the sidebar;
  reach them via Add buttons on parent detail pages. URLs and detail
  pages preserved.
- **BD subnet table** gains a linkified `Gateway (IPAM)` column; the
  legacy column is now labelled `Gateway (legacy)`. Both are in
  `default_columns` with IPAM first.

### Deprecated

- `ACIBridgeDomainSubnet.gateway_ip` (free-form `CharField`). Existing
  rows continue to round-trip and the field stays visible in forms,
  tables, and the API throughout the 0.2.x line. A future major
  release will remove it; new subnets should use
  `gateway_ipam_ip_address` instead.

### Internal

- **CI test scanner hardening.** The `test_form_dropdown_filters`
  regex used a nested-paren alternation that backtracked
  exponentially on a `DynamicModelChoiceField` whose body contained
  a nested `_("...")` call. Replaced with a paren-counting walker;
  the same forms now scan in milliseconds.

---

## [0.1.5] — 2026-05-29

Patch release finishing the device ACI Context restyle: the **L3Out
Logical Nodes** sub-card now follows the same per-attribute
`attr-table` layout as the rest of the panel.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Changed

- **L3Out Logical Nodes sub-card restyled to per-node `attr-table`**
  (PR #21). The v0.1.4 restyle missed one section: each logical node
  on the device ACI Context panel was rendered as a single attr-table
  row whose right cell stuffed three pieces of data inline
  (`L3Out: ... · Router ID: 1.1.1.1` and a `No static routes.`
  sentence). Each logical node now renders as its own per-attribute
  attr-table inside the section card, with explicit rows for **Logical
  Node**, **L3Out**, **Logical Node Profile**, **Router ID**,
  **Loopback Address**, and **Static Routes**. Consecutive nodes are
  separated by a thin `<hr>` and the card header gains a count badge.
  Empty values render as em-dashes; FK references render as links.
  Pure template + test change.

---

## [0.1.4] — 2026-05-28

Patch release restyling the **Cisco ACI Context** panel on the
`dcim.Device` and `dcim.Interface` detail pages to match NetBox's
stock card layout.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Changed

- **"Cisco ACI Context" panel restyled to NetBox `attr-table`**
  (PR #19). Both the device and interface PluginTemplateExtensions
  now render the same compact two-column label-to-value definition
  list NetBox uses for stock cards like "Device Type" — link-colored
  FK values via `|linkify` and em-dashes for empty fields via
  `|placeholder`. Subordinate sections (Static Port Bindings, L3Out
  Logical Nodes, Reachable Subnets, Contracts, L3Out Interfaces, BGP
  Peers) split into their own cards stacked beneath the summary,
  each with a count badge in the header. Same data density, same
  links, but the panels now blend seamlessly into the surrounding
  NetBox UI. Pure template-layer change; no model, migration, API,
  or serializer impact.

---

## [0.1.3] — 2026-05-27

Patch release adding the AAEP→EPG encap-VLAN reachability check and
fixing a cosmetic em-dash render on the VLAN Pool detail page.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Added

- **AAEP→EPG encap VLAN must be reachable through the AAEP's domains**
  (PR #17). `ACIAAEPEPGMapping.clean()` now resolves the chain
  `AAEP → ACIAAEPDomainAssociation → ACIDomain → ACIVLANPool` and
  asserts the encap is contained in at least one `ACIVLANPoolBlock`
  under those pools. Mirrors APIC's deployment-time behaviour: the
  leaves refuse to program a mapping whose encap isn't covered by any
  bound pool. The check is intentionally permissive while the AAEP is
  still being built (no domains attached, or attached domains have no
  pool yet) so users aren't blocked during incremental config. Eight
  new test cases cover the empty-domain, no-pool, in-range,
  boundary, multi-block, and multi-domain branches.

### Fixed

- **`\u2014` rendering as literal text on the VLAN Pool detail page**
  (PR #17). `templates/netbox_cisco_aci/acivlanpool.html` had a
  `default:"\u2014"` filter call that I'd written assuming the Django
  template engine would interpret the Python escape. It doesn't, so
  the page rendered the literal six characters next to each VLAN
  block. Replaced with the canonical NetBox `|placeholder` filter
  which renders an em-dash in the muted class. Spot-audited the rest
  of the templates — no other instance of this shape.

---

## [0.1.2] — 2026-05-27

Patch release fixing the **Add USeg Attribute** form. All v0.1.x users
who use uSeg EPGs should upgrade.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Fixed

- **"Select a valid choice" on the Add USeg Attribute form (PR #15).**
  `ACIUSegAttributeForm.aci_endpoint_group` restricted the form's
  validation queryset to `ACIEndpointGroup.objects.filter(is_useg=True)`,
  but NetBox's `DynamicModelChoiceField` typeahead fetches candidates
  from the REST API, which had no `is_useg` default. Users saw every
  EPG in the dropdown, picked one that wasn't uSeg, and the form
  rejected the choice on submit. Fixed by adding
  `query_params={"is_useg": True}` to the three affected fields
  (`ACIUSegAttributeForm`, `ACIUSegAttributeBulkEditForm`,
  `ACIUSegAttributeFilterForm`).

### Added

- **`tests/test_form_dropdown_filters.py`** — regression guard. A pure
  static scan that walks every `forms/*.py` and asserts every
  `DynamicModelChoiceField` / `DynamicModelMultipleChoiceField` with a
  filtered queryset (`.filter(…)`) also passes `query_params={…}`. The
  check runs in ~15 ms with no DB setup, and the failure message
  points the next maintainer at the offending field. Designed to
  catch the same class of bug across all future forms.

---

## [0.1.1] — 2026-05-27

Patch release fixing a production-blocking 500 on every list / detail
page in v0.1.0. All v0.1.0 users should upgrade.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Fixed

- **`NoReverseMatch` 500 on every UI page.** NetBox 4.x's object detail
  and list-row templates reverse `<label>_changelog` and
  `<label>_journal` unconditionally for every model, but the plugin's
  `_crud()` URL factory only registered the eight basic CRUD verbs.
  The first time a logged-in user opened any list or detail page,
  NetBox tried to render the per-row dropdown, hit
  `django.urls.exceptions.NoReverseMatch`, and produced a red 500. The
  factory now registers the two missing routes (`changelog`, `journal`)
  for every model, backed by NetBox's stock `ObjectChangeLogView` and
  `ObjectJournalView` (PR #13). The bug existed for every model in
  v0.1.0 — not just `ACIFabric`.

### Added

- **`tests/test_urls.py`** — regression guard. Enumerates every
  UI-bearing model in the plugin and asserts every route in the
  ten-route block (list / add / import / bulk-edit / bulk-delete /
  detail / edit / delete / changelog / journal) reverses cleanly. The
  test class explicitly checks `changelog` and `journal` so a future
  regression of this exact bug fails the build with an obvious error.
  CI did not catch the original failure because NetBox's
  `ViewTestCases` and `APIViewTestCases` only reverse the explicit
  verbs they cover — they never touch `*_changelog` or `*_journal`.

---

## [0.1.0] — 2026-05-26

First public release.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12 only
> (NetBox 4.5+ requires Python 3.12).

This release models every ACI construct needed for daily operations
across seven build phases, plus end-to-end NetBox plugin surface
(forms / tables / filtersets / UI views / REST API / GraphQL / search /
navigation / template extensions / migrations / 1,245+ tests) on a
Cloud / Kubernetes-friendly footprint.

### Added — Fabric topology (Phase 1)

- `ACIFabric`, `ACIPod`, `ACINode` (with optional generic foreign key to
  either `dcim.Device` or `virtualization.VirtualMachine`).
- Per-fabric uniqueness on pods; per-pod uniqueness on nodes; multi-fabric
  deployments and overlapping fabric IDs both supported.

### Added — Tenancy (Phase 2)

- `ACITenant`, `ACIVRF` (optional FK to `ipam.VRF`), `ACIBridgeDomain`
  with full L2/L3 forwarding policy and `ACIBridgeDomainSubnet`
  (gateway IP, scope flags, optional FK to `ipam.Prefix`).
- `ACIAppProfile`, `ACIEndpointGroup` (with `is_useg`, intra-EPG isolation,
  preferred-group, admin-shutdown, QoS), `ACIUSegAttribute` (only valid
  on uSeg EPGs), `ACIEndpointSecurityGroup` (VRF-scoped).
- BD-Tenant / VRF-Tenant / AP-Tenant agreement enforced; `common`-tenant
  carve-out for shared VRFs and contracts.

### Added — Access policies, Phase A (Phase 3)

- `ACIVLANPool` + `ACIVLANPoolBlock` (overlap refused inside a pool,
  allowed across pools).
- `ACIDomain` — single model for all five APIC domain types (Physical,
  L3, VMM, L2-Ext, FC) via `domain_type`.
- `ACIAAEP` + `ACIAAEPDomainAssociation` through-model + `ACIAAEPEPGMapping`,
  all cross-fabric guarded.

### Added — Access policies, Phase B (Phase 4)

- Six per-port policy templates: `ACILinkLevelPolicy`, `ACICDPInterfacePolicy`,
  `ACILLDPInterfacePolicy`, `ACILACPInterfacePolicy`, `ACIMCPInterfacePolicy`,
  `ACISTPInterfacePolicy`.
- `ACIInterfacePolicyGroup` (Access / PC / vPC) with nullable FKs to each
  of the six per-port policies plus AAEP, and a cross-fabric guard on
  every reference.
- `ACISwitchProfile` + `ACISwitchProfileSelector` (range or all-leaves).
- `ACIInterfaceProfile` + `ACIInterfaceProfileSelector` (module / port
  range, bound to a Policy Group).
- `ACISwitchProfileInterfaceProfileAttachment` linking the two profiles
  with a cross-fabric guard.

### Added — Contracts (Phase 5)

- `ACIContract` (per-tenant, `scope`, optional `qos_class`).
- `ACISubject` with a `reverse_filter_ports` guard active only when
  `apply_both_directions` is true.
- `ACIFilter` + `ACIFilterEntry` with strict validation: TCP/UDP port
  pairs require both sides, ARP opcode only on `ether_type='arp'`,
  ICMP type/code only on `ip_protocol in {'icmp','icmpv6'}`.
- `ACISubjectFilter` through-model with optional `direction` / `action` /
  `priority` overrides.
- `ACIContractRelation` through-model attaching a Contract as provider,
  consumer, or taboo to an EPG **xor** ESG **xor** External EPG.

### Added — Static port bindings + device/interface visibility (Phase 6)

- `ACIStaticPortBinding` — binds an EPG to a `dcim.Interface` with encap
  VLAN, binding type (`regular` / `pc` / `vpc`), mode, primary encap
  VLAN (uSeg only), and deployment immediacy.
- `ACIVPCBindingPair` — groups two `ACIStaticPortBinding`s as the two
  leaf sides of a single vPC with same-EPG / same-encap / different-device
  guards.
- `ACIDomainBinding` — APIC `fvRsDomAtt` equivalent binding an EPG to an
  `ACIDomain` with deployment / resolution immediacy.
- `ACIInterfaceFabricMembership` — per-interface ACI Node attribution.
- Auto-derived APIC-policy-safe `name` for all binding models via
  `Model.save()` and matching API serializer logic.
- **PluginTemplateExtensions** on `dcim.Device` and `dcim.Interface`
  inject "Cisco ACI Context" panels surfacing the EPGs, BDs, subnets,
  VRFs, and contracts touching the hardware.

### Added — L3Outs (Phase 7)

- `ACIL3Out` with per-protocol enablement (BGP / OSPF / EIGRP / Static).
- `ACILogicalNodeProfile` + `ACILogicalNode` (border-leaf pinning with
  router IDs and loopbacks).
- `ACILogicalInterfaceProfile` (routed / sub-interface / SVI / floating-SVI
  variants with encap and MTU) + `ACIL3OutInterface` binding logical
  interfaces to physical `dcim.Interface` rows with primary and secondary
  IP addresses.
- `ACIBGPPeer` (attaches at either LIP or LNP scope; full BGP / peer /
  address-family / private-ASN control bitmaps and MD5 auth).
- `ACIOSPFInterfacePolicy` + `ACIOSPFInterfaceAttachment` (reusable
  per-tenant OSPF policies attached to LIPs with area ID / type / cost).
- `ACIEIGRPInterfacePolicy` (per-tenant EIGRP timers + controls).
- `ACIExternalEPG` + `ACIExternalEPGSubnet` (route-leak / security scope
  controls per prefix).
- `ACIL3OutStaticRoute` + `ACIL3OutStaticRouteNextHop` (per-node static
  routes with prefix / preference / track policy / BFD; per-route
  next-hop entries supporting both prefix and null-route types, with
  per-hop preference for ECMP weighting).
- Device and Interface "Cisco ACI Context" panels extended to surface
  L3Out attachments and static routes.

### Added — Infrastructure and governance

- **Cloud / Kubernetes compatibility contract.** Documented in
  `docs/cloud-compatibility.md` and `AGENTS.md`; enforced by the
  `cloud-compat` CI job (`scripts/check_cloud_compat.py`) — local
  filesystem writes, in-process threading or schedulers, subprocess use,
  Django management commands, file-based caches, and hard-coded host
  paths all fail the build.
- `AGENTS.md` and `CLAUDE.md` for AI-assisted development.
- `COMPATIBILITY.md` per the NetBox plugin catalogue standard.
- `MkDocs Material` documentation site built from `docs/` and deployed
  to GitHub Pages on every push to `main`.
- GitHub Actions release workflow (`.github/workflows/release.yml`)
  that publishes to PyPI on tag push, supporting both trusted publishing
  (OIDC) and `PYPI_API_TOKEN` flows, and creates a GitHub Release from
  the matching CHANGELOG section.
- Codecov upload integrated into the test matrix.

### CI

- Matrix: NetBox 4.5 × Python 3.12 and NetBox 4.6 × Python 3.12.
  (NetBox 4.5+ requires Python 3.12, so a 3.11 matrix entry would only
  re-run the lint paths and is intentionally omitted.)
- `cloud-compat`, `lint` (ruff `0.15.14` pinned), and the two NetBox
  test jobs are all required checks on `main`.
- Coverage reporting via `coverage[toml]` with an initial gate of 65%
  (`--cov-fail-under=65` re-enabled now that the model surface is stable
  at v0.1.0).

### Notes

- 1,245+ tests across models, forms, filtersets, REST API, and template
  extensions; all green on NetBox 4.5 and 4.6.
- `netbox-aci` was already taken on PyPI by an unrelated v0.0.7 project,
  so this plugin ships under the **`netbox-cisco-aci`** distribution
  name. Python package, Django app label, URL base, and constraint
  names all use the matching `netbox_cisco_aci` / `cisco-aci` prefixes.

[Unreleased]: https://github.com/droolingtaz/netbox-cisco-aci/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.5
[0.1.4]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.4
[0.1.3]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.3
[0.1.2]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.2
[0.1.1]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.1
[0.1.0]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.0
