# Compatibility matrix

This page mirrors
[`COMPATIBILITY.md`](https://github.com/droolingtaz/netbox-cisco-aci/blob/main/COMPATIBILITY.md)
at the repo root, which is the source of truth checked by the NetBox
plugin catalogue.

| Plugin version | NetBox versions | Python | Status     |
| ---            | ---             | ---    | ---        |
| `0.2.x`        | 4.6.x           | 3.12   | Current    |
| `0.1.x`        | 4.5.x, 4.6.x    | 3.12   | Historical |

## NetBox 4.6 only (v0.2.0+)

Starting with v0.2.0, the plugin requires **NetBox 4.6.x only**. NetBox 4.5
support was dropped as a breaking change. CI runs the full test suite
against the latest patch of each supported NetBox minor on every push and
pull request.

## Forward compatibility

Future NetBox 4.7+ support will require:

1. Bumping `max_version` in `netbox_cisco_aci/__init__.py`.
2. Adding the new NetBox version to the CI matrix.
3. Cutting a new release line.

## NetBox Enterprise and NetBox Cloud

The plugin runs unmodified on both. See
[Cloud / Kubernetes compatibility](cloud-compatibility.md) for the
hard contract this is built on.
