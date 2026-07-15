---
source: platform
url: https://platform.claude.com/docs/en/api/admin/invites/delete
fetched_at: 2026-07-15T03:08:15.897796Z
sha256: 31cf60aed6d9184d034253d26b4cbb06f9a36c4aa65de453ea16ed0729423053
---

## Delete Invite

**delete** `/v1/organizations/invites/{invite_id}`

For Claude Enterprise organizations, this endpoint's availability is in beta.

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
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

#### Response

```json
{
  "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
  "type": "invite_deleted"
}
```
