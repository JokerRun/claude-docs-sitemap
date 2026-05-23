---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/skills/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 2bcc17a21061848f138191ba24c7b4f4bc42ed64b8d23118126af7767b19d0df
---

## Delete Skill

`$ ant beta:skills delete`

**delete** `/v1/skills/{skill_id}`

Delete Skill

### Parameters

- `--skill-id: string`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `BetaSkillDeleteResponse: object { id, type }`

  - `id: string`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `type: string`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

### Example

```cli
ant beta:skills delete \
  --api-key my-anthropic-api-key \
  --skill-id skill_id
```

#### Response

```json
{
  "id": "skill_01JAbcdefghijklmnopqrstuvw",
  "type": "type"
}
```
