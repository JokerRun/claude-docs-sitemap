---
source: platform
url: https://platform.claude.com/docs/en/api/skills/delete
fetched_at: 2026-08-21T02:32:13.524433Z
sha256: 9efb7643732e8985e296160f3d17925d827f8066cc21725bf42a4f080824c456
---

---
title: Delete Skill
url: https://platform.claude.com/docs/en/api/skills/delete
---

## Delete Skill

**delete** `/v1/skills/{skill_id}`

Delete Skill

### Path Parameters

- `skill_id: string`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

### Returns

- `DeletedSkill object { id, type }`

  - `id: string`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `type: "skill_deleted"`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

    - `"skill_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/skills/$SKILL_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

#### Response

```json
{
  "id": "skill_01JAbcdefghijklmnopqrstuvw",
  "type": "skill_deleted"
}
```
