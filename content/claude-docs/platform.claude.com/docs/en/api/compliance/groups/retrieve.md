---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/groups/retrieve
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 1428eeff5c24e6afb8e968d06b017e2c201f0ff53d73c8aad6f4b93f664f9475
---

## Get Compliance Group

**get** `/v1/compliance/groups/{group_id}`

Get Compliance Group

### Path Parameters

- `group_id: string`

  The group ID (tagged ID, e.g., rbac_group_abc123)

### Header Parameters

- `"x-api-key": optional string`

### Returns

- `id: string`

  Group identifier (tagged ID)

- `created_at: string`

  Group creation timestamp (ISO 8601)

- `description: string`

  Group description

- `name: string`

  Group name

- `roles: array of string`

  Role IDs assigned to this group.

- `source_type: string`

  How the group was created ('direct' or 'scim')

- `updated_at: string`

  Group last-updated timestamp (ISO 8601)

### Example

```http
curl https://api.anthropic.com/v1/compliance/groups/$GROUP_ID \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

#### Response

```json
{
  "id": "id",
  "created_at": "created_at",
  "description": "description",
  "name": "name",
  "roles": [
    "string"
  ],
  "source_type": "source_type",
  "updated_at": "updated_at"
}
```
