---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/memory_stores/delete
fetched_at: 2026-04-24T03:12:20.532875Z
sha256: 8a40f4429c08c485cd5bdd093b7f941c432ed4cd339dee62e143a741050fdb21
---

## Delete

`$ ant beta:memory-stores delete`

**delete** `/v1/memory_stores/{memory_store_id}`

DeleteMemoryStore

### Parameters

- `--memory-store-id: string`

  Path parameter memory_store_id

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_managed_agents_deleted_memory_store: object { id, type }`

  - `id: string`

  - `type: "memory_store_deleted"`

    - `"memory_store_deleted"`

### Example

```cli
ant beta:memory-stores delete \
  --api-key my-anthropic-api-key \
  --memory-store-id memory_store_id
```
