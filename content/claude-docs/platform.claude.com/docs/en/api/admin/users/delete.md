---
source: platform
url: https://platform.claude.com/docs/en/api/admin/users/delete
fetched_at: 2026-07-15T03:08:15.897796Z
sha256: cfb516e46bd1f1074ae3f6c5bd067f7d538f2947dbf2775cbea201bf977f58f0
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
