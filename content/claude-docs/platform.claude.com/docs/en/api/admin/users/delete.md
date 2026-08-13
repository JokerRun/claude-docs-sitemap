---
source: platform
url: https://platform.claude.com/docs/en/api/admin/users/delete
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: aa22cb4c239f82978dd9c0fed02db84751931c99cf0a8edad11abebead4d1ba5
---

---
title: Remove User
url: https://platform.claude.com/docs/en/api/admin/users/delete
---

## Remove User

**delete** `/v1/organizations/users/{user_id}`

For Claude Enterprise organizations, this endpoint's availability is in beta.

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

### Example

```http
curl https://api.anthropic.com/v1/organizations/users/$USER_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

#### Response

```json
{
  "id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
  "type": "user_deleted"
}
```
