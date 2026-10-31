---
source: platform
url: https://platform.claude.com/docs/en/api/organization/users/remove
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: b35780b14e8dc468e4e932a4774da2d679cd3c4829d30a85d26f93ac9f1162f5
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

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning?sdk_languages=http).

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
    -H 'anthropic-version: 2026-10-21' \
    -H "Authorization: Bearer $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "type": "user_deleted"
}
```
