---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/users/remove
fetched_at: 2026-08-27T03:51:55.831897Z
sha256: 3d3550735db23eeb97a264918779ac5b343b87872b2780e5d2763c46ab3e823f
---

# Remove User

**DELETE** `/v1/organizations/users/{user_id}`

Remove a member from the organization.

## Path parameters

- `user_id: string`

  ID of the User.

## Returns

- `id: string`

  ID of the User.

- `type: "user_deleted"`

  Deleted object type.

  For Users, this is always `"user_deleted"`.

  default: user_deleted

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
