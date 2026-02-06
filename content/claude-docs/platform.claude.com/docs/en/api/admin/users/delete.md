---
source: platform
url: https://platform.claude.com/docs/en/api/admin/users/delete
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: fbc1a9c080f0f8edb353e6e21fa7126cc060bc1f9d925feb801aa3207de0d89e
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

### Example

```http
curl https://api.anthropic.com/v1/organizations/users/$USER_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```
