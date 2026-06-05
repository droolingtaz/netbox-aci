# Compatibility Matrix

| Plugin release | NetBox versions | Python | Status  |
|----------------|-----------------|--------|---------|
| `0.2.x`        | 4.6.x           | 3.12   | Current |
| `0.1.x`        | 4.5.x, 4.6.x    | 3.12   | Historical |

Starting with v0.2.0 the plugin requires **NetBox 4.6.x only**. NetBox 4.5
support was dropped. CI runs the full test suite against the latest patch
of each supported NetBox minor on every push.

When NetBox 4.7 ships, this matrix gets a new row; the 4.6 row stays
frozen so existing deployments have a clear pin target.
