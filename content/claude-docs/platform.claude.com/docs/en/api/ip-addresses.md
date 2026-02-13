---
source: platform
url: https://platform.claude.com/docs/en/api/ip-addresses
fetched_at: 2026-02-13T04:23:55.295784Z
sha256: 2801630b1acad57c7fa2b7e1b839e261a2c523dd9beadbb4610523fd885bd30b
---

# IP addresses

Anthropic services use fixed IP addresses for both inbound and outbound connections. You can use these addresses to configure your firewall rules for secure access to the Claude API and Console. These addresses will not change without notice.

---

## Inbound IP addresses

These are the IP addresses where Anthropic services receive incoming connections.

#### IPv4

`160.79.104.0/23`

#### IPv6

`2607:6bc0::/48`

## Outbound IP addresses

These are the stable IP addresses that Anthropic uses for outbound requests (for example, when making MCP tool calls to external servers).

#### IPv4

`160.79.104.0/21`

*The following individual IP addresses are still in use, but will be phased out starting January 15, 2026.*

```text
34.162.46.92/32
34.162.102.82/32
34.162.136.91/32
34.162.142.92/32
34.162.183.95/32
```