# netbox-cisco-aci

A [NetBox](https://netboxlabs.com/oss/netbox/) plugin for **operational
visibility and documentation of Cisco ACI** fabrics.

Models every ACI construct an operator touches on day one: physical
topology, tenancy, access policies, contracts, L3Outs, and the
fabric-wide pod policies (NTP, syslog, SNMP, SNMP traps, BGP route
reflector, COOP, IS-IS) that apply to every pod via a Pod Policy
Group and Pod Profile. Includes per-interface EPG / BD / Subnet
bindings so you can see the ACI policy applied to any device or port
at a glance.

[![CI](https://github.com/droolingtaz/netbox-cisco-aci/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/droolingtaz/netbox-cisco-aci/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/droolingtaz/netbox-cisco-aci/branch/main/graph/badge.svg?precision=1)](https://app.codecov.io/gh/droolingtaz/netbox-cisco-aci)
[![PyPI](https://img.shields.io/pypi/v/netbox-cisco-aci?label=pypi&logo=pypi&logoColor=white)](https://pypi.org/project/netbox-cisco-aci/)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://pypi.org/project/netbox-cisco-aci/)
[![NetBox](https://img.shields.io/badge/netbox-4.6-26a69a.svg)](COMPATIBILITY.md)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-526CFE.svg)](https://droolingtaz.github.io/netbox-cisco-aci/)

## Compatibility

NetBox v4.6 only, Python 3.12. See the [compatibility matrix](COMPATIBILITY.md)
for the exact pinning policy.

The plugin is designed to run unmodified on **NetBox Enterprise** and
**NetBox Cloud** (both Kubernetes-based, multi-pod, immutable
filesystems) as well as classic single-VM installs. The contract is
documented in [`docs/cloud-compatibility.md`](docs/cloud-compatibility.md)
and enforced by the `cloud-compat` CI job.

## Features

The plugin's navigation mirrors how an ACI operator actually structures
work in APIC. Each group below maps 1:1 to a sidebar group in NetBox.

### Fabric

- **Fabric → Pod → Node**, with each Node optionally linked to a
  `dcim.Device` so existing inventory remains the source of truth for
  hardware.

### Tenancy

- **Tenant → VRF, Bridge Domain (+ Subnets)** — BD Subnets carry both
  a free-form `gateway_ip` and an IPAM-linked `gateway_ipam_ip_address`
  FK so gateways can participate in NetBox IPAM utilisation and audit
  reporting.
- **Application Profile → EPG / ESG**, including uSeg attributes.
- Validations: encap-VLAN check on static port bindings, External EPG
  duplicate-prefix-in-VRF check, AAEP overlapping-VLAN check.

### Connectivity (Access Policies)

- **VLAN Pools, Physical / L3 / VMM Domains, AAEPs** with EPG mappings.
- **Switch Profiles, Interface Profiles, Interface Policy Groups**, and
  per-policy refs (CDP / LLDP / LACP / MCP / STP / Link Level).
- **Per-interface bindings** — every static port binding links an EPG
  to a `dcim.Interface`. The plugin injects panels on both the Device
  and Interface detail views showing the EPGs, BDs, Subnets, and VRFs
  that touch that hardware.

### Contracts

- **Contracts, Subjects, Filters with entries**, and Provider / Consumer
  relations (including `common`-tenant imports and inter-VRF /
  shared-services patterns).

### L3Outs

- **Logical Node Profiles, Logical Interface Profiles** (routed / SVI /
  sub-interface), **BGP / OSPF / EIGRP peers**, **External EPGs** with
  subnets and contract bindings.
- **BFD** — `ACIBFDInterfacePolicy` and per-interface attachments for
  the L3Out logical-interface profiles that need it.
- `PLUGINS_CONFIG['netbox_cisco_aci']['l3out_default_protocols']`
  seeds the L3Out protocol checkboxes at site level.

### Pod Policies

The fabric-wide monitoring and control-plane policies that APIC's
pod-policy-group bundles together and applies to every pod:

- **Pod Profile + Pod Selector** (`fabricPodP` / `fabricPodS`) — the
  binding layer. A selector is range/ALL and points at exactly one
  Pod Policy Group.
- **Pod Policy Group** (`fabricPodPGrp`) — the central row that links
  one policy of each type below.
- **NTP** — policy + per-provider list, with min/max poll, key-ID,
  and a partial-unique constraint enforcing "at most one preferred
  provider per policy".
- **Syslog** — policy + remote destinations with per-destination
  severity and forwarding facility.
- **SNMP** — policy + communities, client groups + clients, and v3
  users. Auth and privacy protocols are recorded for visibility;
  passphrases stay on APIC.
- **SNMP Traps** — policy + forwarder destinations, with `version=v3`
  guarded by a `clean()` check on `v3_security_level`.
- **BGP Route Reflector** — policy + per-spine-node list
  (`bgpRRP` / `bgpRRNodePEp`).
- **COOP Group** — strict / compatible MD5 authentication between
  spines.
- **IS-IS Domain** — metric style, LSP timers, fast-flood.
- **Date/Time** — reuses the NTP policy model, since APIC's
  `datetimePol` MO has the same shape.

### Platform integration

- **Full NetBox surface** — REST API, GraphQL, search, navigation,
  change-logging, journal, custom fields, tags, and per-object RBAC.
- **CI-enforced cloud compatibility** — the `cloud-compat` job blocks
  any pattern that would break on NetBox Cloud / Enterprise.

## Installation

```bash
source /opt/netbox/venv/bin/activate
pip install netbox-cisco-aci
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`:

```python
PLUGINS = ['netbox_cisco_aci']
```

Run migrations and restart NetBox:

```bash
python /opt/netbox/netbox/manage.py migrate
sudo systemctl restart netbox netbox-rq
```

Add `netbox-cisco-aci` to `local_requirements.txt`.

## Configuration

The plugin works with sensible defaults. Optional settings live under
`PLUGINS_CONFIG['netbox_cisco_aci']` — see the [configuration docs](docs/configuration.md).

## Development

See [AGENTS.md](AGENTS.md) for repository conventions and
[docs/development.md](docs/development.md) for the dev-loop quickstart.

## Licensing

Apache License 2.0 — see [LICENSE](LICENSE).
