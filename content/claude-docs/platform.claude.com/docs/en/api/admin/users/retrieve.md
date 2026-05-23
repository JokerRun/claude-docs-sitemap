---
source: platform
url: https://platform.claude.com/docs/en/api/admin/users/retrieve
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 2e9989822a983efaef1ee5ab84ba2a71cf014a76805b2f1322260b59e6190690
---

## Get User

**get** `/v1/organizations/users/{user_id}`

Get User

### Path Parameters

- `user_id: string`

  ID of the User.

### Returns

- `User object { id, added_at, email, 3 more }`

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

    - `"user"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/users/$USER_ID \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

#### Response

```json
{
  "id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
  "added_at": "2024-10-30T23:58:27.427722Z",
  "email": "user@emaildomain.com",
  "name": "Jane Doe",
  "role": "user",
  "type": "user"
}
```
