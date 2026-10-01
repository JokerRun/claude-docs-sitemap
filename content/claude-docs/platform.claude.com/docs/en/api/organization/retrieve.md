---
source: platform
url: https://platform.claude.com/docs/en/api/organization/retrieve
fetched_at: 2026-10-01T02:31:31.030823Z
sha256: a947d9db9d800caaf4a53336a25304d4d83b768d268a9febe219e6da7ec1ec2b
---

---
title: Get Current Organization
url: https://platform.claude.com/docs/en/api/organization/retrieve
---

# Get Current Organization

**GET** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

## Returns

- `OrganizationInfo object`

  - `type: "organization"`

    Object type.

    For Organizations, this is always `"organization"`.

    default: organization

  - `id: string`

    ID of the Organization.

    format: uuid

  - `name: string`

    Name of the Organization.

## Example

```bash
curl https://api.anthropic.com/v1/organizations/me \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "name": "Organization Name",
  "type": "organization"
}
```
