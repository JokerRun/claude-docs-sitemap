---
source: platform
url: https://platform.claude.com/docs/en/api/admin/spend_limits/delete
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 7d2790ca4cc8d6cafa376057cc3507e8ebe049bdd1191dc9cf4436640a7615ef
---

---
title: Delete Spend Limit
url: https://platform.claude.com/docs/en/api/admin/spend_limits/delete
---

## Delete Spend Limit

**delete** `/v1/organizations/spend_limits/{spend_limit_id}`

Delete a per-user spend limit override.

The member falls back to any inherited spend limit at that period.
Seat-tier, group, and organization-level rows cannot be deleted via
this endpoint.

### Path Parameters

- `spend_limit_id: string`

  ID of the Spend Limit.

### Returns

- `id: string`

- `type: "spend_limit_deleted"`

  - `"spend_limit_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/spend_limits/$SPEND_LIMIT_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

#### Response

```json
{
  "id": "id",
  "type": "spend_limit_deleted"
}
```
