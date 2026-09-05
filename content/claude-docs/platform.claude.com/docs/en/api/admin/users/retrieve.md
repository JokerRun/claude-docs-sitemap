---
source: platform
url: https://platform.claude.com/docs/en/api/admin/users/retrieve
fetched_at: 2026-09-05T02:20:11.001334Z
sha256: ff6ba6c0515c6127202ef30cc9cd1a9eddbc60f649bf274e1b0d173c1e11af10
---

# Get User

**GET** `/v1/organizations/users/{user_id}`

Retrieve a member of the organization by user ID.

## Path parameters

- `user_id: string`

  ID of the User.

## Returns

- `User object`

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

    format: date-time

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "admin" or "billing" or "claude_code_user" or 6 more`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

    default: user

## Example

```bash
curl https://api.anthropic.com/v1/organizations/users/$USER_ID \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN"
```

### Response (200)

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
