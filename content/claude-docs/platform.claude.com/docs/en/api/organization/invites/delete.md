---
source: platform
url: https://platform.claude.com/docs/en/api/organization/invites/delete
fetched_at: 2026-10-01T02:31:31.030823Z
sha256: ede1f16df7613180c48ed827f44f4d1d3956812a716e91131c36d07e10ca90bb
---

---
title: Delete Invite
url: https://platform.claude.com/docs/en/api/organization/invites/delete
---

# Delete Invite

**DELETE** `/v1/organizations/invites/{invite_id}`

Delete a pending invite.

## Path parameters

- `invite_id: string`

  ID of the Invite.

## Returns

- `type: "invite_deleted"`

  Deleted object type.

  For Invites, this is always `"invite_deleted"`.

  default: invite_deleted

- `id: string`

  ID of the Invite.

## Example

```bash
curl https://api.anthropic.com/v1/organizations/invites/$INVITE_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
  "type": "invite_deleted"
}
```
