---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/sessions/resources/delete
fetched_at: 2026-04-09T03:10:22.306859Z
sha256: 3b1c71ebc944de47fc103acfab6515dec1fef66e783b6752bce5856aef67e4a4
---

## Delete

`$ ant beta:sessions:resources delete`

**delete** `/v1/sessions/{session_id}/resources/{resource_id}`

Delete Session Resource

### Parameters

- `--session-id: string`

  Path param: Path parameter session_id

- `--resource-id: string`

  Path param: Path parameter resource_id

- `--beta: optional array of AnthropicBeta`

  Header param: Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_managed_agents_delete_session_resource: object { id, type }`

  Confirmation of resource deletion.

  - `id: string`

  - `type: "session_resource_deleted"`

    - `"session_resource_deleted"`

### Example

```cli
ant beta:sessions:resources delete \
  --api-key my-anthropic-api-key \
  --session-id sesn_011CZkZAtmR3yMPDzynEDxu7 \
  --resource-id sesrsc_011CZkZBJq5dWxk9fVLNcPht
```
