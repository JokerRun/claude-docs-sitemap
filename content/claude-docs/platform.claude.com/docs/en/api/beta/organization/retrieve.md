---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/retrieve
fetched_at: 2026-10-13T02:33:54.812386Z
sha256: c8ec3b45f65348c8a1930c2ff1511b101ab1030a55c639db372af42e881bcc95
---

---
title: Get Current Organization
url: https://platform.claude.com/docs/en/api/beta/organization/retrieve
---

# Get Current Organization

**GET** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning?sdk_languages=http).

## Returns

- `BetaOrganization object`

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
