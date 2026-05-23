---
source: platform
url: https://platform.claude.com/docs/en/api/admin/organizations/me
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: bf422d9165750fbac5abf788ad675d569b3203092f91d0c7ec8be7af8437a136
---

## Get Current Organization

**get** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

### Returns

- `Organization object { id, name, type }`

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
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

#### Response

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "name": "Organization Name",
  "type": "organization"
}
```
