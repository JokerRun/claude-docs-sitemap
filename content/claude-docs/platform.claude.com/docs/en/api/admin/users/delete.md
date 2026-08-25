---
source: platform
url: https://platform.claude.com/docs/en/api/admin/users/delete
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: c3c935dc334aa6822f5034985266ef5dd43db118ad06dd81334a0af3de2f74d4
---

# Remove User

**DELETE** `/v1/organizations/users/{user_id}`

For Claude Enterprise organizations, this endpoint's availability is in beta.

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
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

### Response (200)

```json
{
  "id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
  "type": "user_deleted"
}
```
