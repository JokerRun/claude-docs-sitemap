---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/memory_stores/archive
fetched_at: 2026-04-24T03:12:20.532875Z
sha256: ffcfb80af373cec13f280d64c7c8a4ec9b9aa428ba3248ffbe5ef556178e22f8
---

## Archive

`$ ant beta:memory-stores archive`

**post** `/v1/memory_stores/{memory_store_id}/archive`

ArchiveMemoryStore

### Parameters

- `--memory-store-id: string`

  Path parameter memory_store_id

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_managed_agents_memory_store: object { id, type, archived_at, 5 more }`

  - `id: string`

  - `type: "memory_store"`

    - `"memory_store"`

  - `archived_at: optional string`

    A timestamp in RFC 3339 format

  - `created_at: optional string`

    A timestamp in RFC 3339 format

  - `description: optional string`

  - `metadata: optional map[string]`

  - `name: optional string`

  - `updated_at: optional string`

    A timestamp in RFC 3339 format

### Example

```cli
ant beta:memory-stores archive \
  --api-key my-anthropic-api-key \
  --memory-store-id memory_store_id
```
