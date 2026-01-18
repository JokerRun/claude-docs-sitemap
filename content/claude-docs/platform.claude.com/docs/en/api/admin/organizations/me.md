---
source: platform
url: https://platform.claude.com/docs/en/api/admin/organizations/me
fetched_at: 2026-01-18T03:48:37.713242Z
sha256: a47a10fa9717fd30e259e2d3278ed601ec43702ae770f823b037827956cf1bb0
---

## Me

**get** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

### Returns

- `Organization = object { id, name, type }`

  - `id: string`

    ID of the Organization.

  - `name: string`

    Name of the Organization.

  - `type: "organization"`

    Object type.

    For Organizations, this is always `"organization"`.

    - `"organization"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/me \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```
