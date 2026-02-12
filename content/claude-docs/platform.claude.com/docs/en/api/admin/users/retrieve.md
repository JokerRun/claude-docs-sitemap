---
source: platform
url: https://platform.claude.com/docs/en/api/admin/users/retrieve
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: ee53f820d7d7b0d8bf692e9a7093896521051fe5e84587536f24691c33ab4f61
---

## Retrieve

**get** `/v1/organizations/users/{user_id}`

Get User

### Path Parameters

- `user_id: string`

  ID of the User.

### Returns

- `User = object { id, added_at, email, 3 more }`

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "user" or "developer" or "billing" or 3 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

    - `"managed"`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

    - `"user"`
