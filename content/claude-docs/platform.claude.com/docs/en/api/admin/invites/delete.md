---
source: platform
url: https://platform.claude.com/docs/en/api/admin/invites/delete
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: da38b2d5a71d25269ef15e8f592503a60a303a4b4f32f84aeba32142894137f9
---

# Delete Invite

**DELETE** `/v1/organizations/invites/{invite_id}`

For Claude Enterprise organizations, this endpoint's availability is in beta.

## Path parameters

- `invite_id: string`

  ID of the Invite.

## Returns

- `id: string`

  ID of the Invite.

- `type: "invite_deleted"`

  Deleted object type.

  For Invites, this is always `"invite_deleted"`.

  default: invite_deleted

## Example

```bash
curl https://api.anthropic.com/v1/organizations/invites/$INVITE_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

### Response (200)

```json
{
  "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
  "type": "invite_deleted"
}
```
