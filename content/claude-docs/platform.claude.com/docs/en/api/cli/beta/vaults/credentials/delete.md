---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/vaults/credentials/delete
fetched_at: 2026-04-09T03:10:22.306859Z
sha256: 9b8d5c30f37b01e891756cfffe1188242033c335d210965a7392b5c95c4c0174
---

## Delete

`$ ant beta:vaults:credentials delete`

**delete** `/v1/vaults/{vault_id}/credentials/{credential_id}`

Delete Credential

### Parameters

- `--vault-id: string`

  Path param: Path parameter vault_id

- `--credential-id: string`

  Path param: Path parameter credential_id

- `--beta: optional array of AnthropicBeta`

  Header param: Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_managed_agents_deleted_credential: object { id, type }`

  Confirmation of a deleted credential.

  - `id: string`

    Unique identifier of the deleted credential.

  - `type: "vault_credential_deleted"`

    - `"vault_credential_deleted"`

### Example

```cli
ant beta:vaults:credentials delete \
  --api-key my-anthropic-api-key \
  --vault-id vlt_011CZkZDLs7fYzm1hXNPeRjv \
  --credential-id vcrd_011CZkZEMt8gZan2iYOQfSkw
```
