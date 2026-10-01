---
source: platform
url: https://platform.claude.com/docs/en/api/organization/users/remove
fetched_at: 2026-10-01T02:31:31.030823Z
sha256: ec4656f4059c3590f39147972b8a00b11066379e607ab0ef316c92719df0db5e
---

---
title: Remove User
url: https://platform.claude.com/docs/en/api/organization/users/remove
---

# Remove User

**DELETE** `/v1/organizations/users/{user_id}`

Remove a member from the organization.

## Path parameters

- `user_id: string`

  ID of the User.

## Returns

- `type: "user_deleted"`

  Deleted object type.

  For Users, this is always `"user_deleted"`.

  default: user_deleted

- `id: string`

  ID of the User.

## Example

```bash
curl https://api.anthropic.com/v1/organizations/users/$USER_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
  "type": "user_deleted"
}
```
