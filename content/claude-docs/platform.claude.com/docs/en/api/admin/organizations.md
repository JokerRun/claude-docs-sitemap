---
source: platform
url: https://platform.claude.com/docs/en/api/admin/organizations
fetched_at: 2026-06-12T03:17:40.104094Z
sha256: b3765a7326fcae47c5f779509b7ab62e84f970af019af069e1ebb5ebd4cd24b5
---

# Organizations

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
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

#### Response

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "name": "Organization Name",
  "type": "organization"
}
```

## Domain Types

### Organization

- `Organization object { id, name, type }`

  - `id: string`

    ID of the Organization.

  - `name: string`

    Name of the Organization.

  - `type: "organization"`

    Object type.

    For Organizations, this is always `"organization"`.

    - `"organization"`
