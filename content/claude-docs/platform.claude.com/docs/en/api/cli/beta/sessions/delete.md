---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/sessions/delete
fetched_at: 2026-04-09T03:10:22.306859Z
sha256: 8e627406a19efed22c9962e3046c1657bc7c3be12e329444328662bf9d55744d
---

## Delete

`$ ant beta:sessions delete`

**delete** `/v1/sessions/{session_id}`

Delete Session

### Parameters

- `--session-id: string`

  Path parameter session_id

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_managed_agents_deleted_session: object { id, type }`

  Confirmation that a `session` has been permanently deleted.

  - `id: string`

  - `type: "session_deleted"`

    - `"session_deleted"`

### Example

```cli
ant beta:sessions delete \
  --api-key my-anthropic-api-key \
  --session-id sesn_011CZkZAtmR3yMPDzynEDxu7
```
