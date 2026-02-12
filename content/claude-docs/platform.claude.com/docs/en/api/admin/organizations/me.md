---
source: platform
url: https://platform.claude.com/docs/en/api/admin/organizations/me
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: 0f7eba6d67fb306efec9878cddabcb3fcc29eab07b6ebfb9edbabd19b5389b5a
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
