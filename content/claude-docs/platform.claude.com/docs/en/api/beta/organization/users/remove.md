---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/users/remove
fetched_at: 2026-09-11T02:21:44.680579Z
sha256: caf1c1af87705e9d04335b28f78184f7851e8f7f59b3b39509225f230600b4e5
---

---
title: Remove User
url: https://platform.claude.com/docs/en/api/beta/organization/users/remove
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
