---
source: platform
url: https://platform.claude.com/docs/en/api/admin/invites/delete
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: 17e962d49b249dcf0fcecf40c329a5a5afa77acc8aa0dbb2d2b20a609c883490
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
