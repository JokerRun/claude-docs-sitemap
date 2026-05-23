---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/vaults/retrieve
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: f42efbd4927f7aa28b14bf9b07df2b2ee5fb14486c2cbfd96827b45d59e07066
---

## Get Vault

`$ ant beta:vaults retrieve`

**get** `/v1/vaults/{vault_id}`

Get Vault

### Parameters

- `--vault-id: string`

  Path parameter vault_id

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_managed_agents_vault: object { id, archived_at, created_at, 4 more }`

  A vault that stores credentials for use by agents during sessions.

  - `id: string`

    Unique identifier for the vault.

  - `archived_at: string`

    A timestamp in RFC 3339 format

  - `created_at: string`

    A timestamp in RFC 3339 format

  - `display_name: string`

    Human-readable name for the vault.

  - `metadata: map[string]`

    Arbitrary key-value metadata attached to the vault.

  - `type: "vault"`

    - `"vault"`

  - `updated_at: string`

    A timestamp in RFC 3339 format

### Example

```cli
ant beta:vaults retrieve \
  --api-key my-anthropic-api-key \
  --vault-id vlt_011CZkZDLs7fYzm1hXNPeRjv
```

#### Response

```json
{
  "id": "vlt_011CZkZDLs7fYzm1hXNPeRjv",
  "archived_at": null,
  "created_at": "2026-03-15T10:00:00Z",
  "display_name": "Example vault",
  "metadata": {
    "environment": "production"
  },
  "type": "vault",
  "updated_at": "2026-03-15T10:00:00Z"
}
```
