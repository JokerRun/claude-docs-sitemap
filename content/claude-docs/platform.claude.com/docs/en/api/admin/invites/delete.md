---
source: platform
url: https://platform.claude.com/docs/en/api/admin/invites/delete
fetched_at: 2026-01-18T03:48:37.713242Z
sha256: 81dfae08c140091ffc93cc928d024ad9edd9b018dc6793235fc67c628361f69e
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
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```
