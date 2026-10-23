---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/invites/delete
fetched_at: 2026-10-23T02:21:28.653315Z
sha256: 8cff664cdb93abf04ec7e5b52fbe7711cb2adc08510a4017110c2fcefb7cb2ae
---

---
title: Delete Invite
url: https://platform.claude.com/docs/en/api/beta/organization/invites/delete
---

# Delete Invite

**DELETE** `/v1/organizations/invites/{invite_id}`

Delete a pending invite.

## Path parameters

- `invite_id: string`

  ID of the Invite.

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning?sdk_languages=http).

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
    -H 'anthropic-version: 2026-10-21' \
    -H "Authorization: Bearer $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
  "type": "invite_deleted"
}
```
