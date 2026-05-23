---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/sessions/resources/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: a66eff16ba49d7559afab5bf97551fc6e1e5567ba5cd2e97c3d44b08069a518c
---

## Delete Session Resource

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

#### Response

```json
{
  "id": "sesrsc_011CZkZBJq5dWxk9fVLNcPht",
  "type": "session_resource_deleted"
}
```
