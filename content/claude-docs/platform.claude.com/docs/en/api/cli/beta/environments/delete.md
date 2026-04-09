---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/environments/delete
fetched_at: 2026-04-09T03:10:22.306859Z
sha256: c517e564e3f32013663fc411666e3552a216c0976a0fbdb06c225f4f9c1ade4a
---

## Delete

`$ ant beta:environments delete`

**delete** `/v1/environments/{environment_id}`

Delete an environment by ID. Returns a confirmation of the deletion.

### Parameters

- `--environment-id: string`

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_environment_delete_response: object { id, type }`

  Response after deleting an environment.

  - `id: string`

    Environment identifier

  - `type: "environment_deleted"`

    The type of response

### Example

```cli
ant beta:environments delete \
  --api-key my-anthropic-api-key \
  --environment-id env_011CZkZ9X2dpNyB7HsEFoRfW
```
