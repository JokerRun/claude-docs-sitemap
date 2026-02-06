---
source: platform
url: https://platform.claude.com/docs/en/api/admin/invites/delete
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 4d77b687fd8984ae05dd0ab1b7d7c770619940ce53da9dcbe8ce4d986648a4d5
---

## Delete

**delete** `/v1/organizations/invites/{invite_id}`

Delete Invite

### Path Parameters

- `invite_id: string`

  ID of the Invite.

### Returns

- `id: string`

  ID of the Invite.

- `type: "invite_deleted"`

  Deleted object type.

  For Invites, this is always `"invite_deleted"`.

  - `"invite_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/invites/$INVITE_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```
