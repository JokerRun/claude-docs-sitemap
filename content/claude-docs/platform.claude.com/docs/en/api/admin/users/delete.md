---
source: platform
url: https://platform.claude.com/docs/en/api/admin/users/delete
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: 24332f9ac0db1f38048a5173bccf527cd9f0f1e216e8805d44ecb58e39a895a0
---

## Delete

**delete** `/v1/organizations/users/{user_id}`

Remove User

### Path Parameters

- `user_id: string`

  ID of the User.

### Returns

- `id: string`

  ID of the User.

- `type: "user_deleted"`

  Deleted object type.

  For Users, this is always `"user_deleted"`.

  - `"user_deleted"`
