---
source: platform
url: https://platform.claude.com/docs/en/api/admin/organizations/me
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: fe63c8e8bf27c1b7b1e1bec480af25e9d5e957793915126c519e8a3d905b4d29
---

# Get Current Organization

**GET** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

## Returns

- `Organization object`

  - `id: string`

    ID of the Organization.

    format: uuid

  - `name: string`

    Name of the Organization.

  - `type: "organization"`

    Object type.

    For Organizations, this is always `"organization"`.

    default: organization

## Example

```bash
curl https://api.anthropic.com/v1/organizations/me \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

### Response (200)

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "name": "Organization Name",
  "type": "organization"
}
```
