---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/memory_stores/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: b93a063e2503b762763b0e6a19ad951cabc9b8a0f0b77f41760794f1528c4f94
---

## Delete a memory store

`$ ant beta:memory-stores delete`

**delete** `/v1/memory_stores/{memory_store_id}`

Delete a memory store

### Parameters

- `--memory-store-id: string`

  Path parameter memory_store_id

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_managed_agents_deleted_memory_store: object { id, type }`

  Confirmation that a `memory_store` was deleted.

  - `id: string`

    ID of the deleted memory store (a `memstore_...` identifier). The store and all its memories and versions are no longer retrievable.

  - `type: "memory_store_deleted"`

    - `"memory_store_deleted"`

### Example

```cli
ant beta:memory-stores delete \
  --api-key my-anthropic-api-key \
  --memory-store-id memory_store_id
```

#### Response

```json
{
  "id": "id",
  "type": "memory_store_deleted"
}
```
