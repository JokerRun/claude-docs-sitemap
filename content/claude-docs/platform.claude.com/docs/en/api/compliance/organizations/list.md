---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/organizations/list
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 6f4165f51213fb60909f3d3e1dfbd846b040d5090ad6a82c8ad5a520ffbe3689
---

## List organizations

**get** `/v1/compliance/organizations`

List organizations under the parent organization.

Returns a list of organizations sorted by creation date in ascending order.
This endpoint does not support pagination and will return an error if the
response would exceed 1,000 organizations.

### Header Parameters

- `"x-api-key": optional string`

### Returns

- `data: array of object { created_at, name, uuid }`

  List of organizations sorted by creation date, ascending

  - `created_at: string`

    Organization creation time (RFC 3339 format)

  - `name: string`

    Organization name

  - `uuid: string`

    Unique identifier for the organization (UUID format)

### Example

```http
curl https://api.anthropic.com/v1/compliance/organizations \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

#### Response

```json
{
  "data": [
    {
      "created_at": "created_at",
      "name": "name",
      "uuid": "uuid"
    }
  ]
}
```
