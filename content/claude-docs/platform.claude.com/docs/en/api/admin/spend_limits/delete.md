---
source: platform
url: https://platform.claude.com/docs/en/api/admin/spend_limits/delete
fetched_at: 2026-06-17T03:17:04.158711Z
sha256: 1e8585de3759cd7a12607f895820d84a91041fbb98009d7d7b3cb3412ccfef67
---

## Delete Spend Limit

**delete** `/v1/organizations/spend_limits/{spend_limit_id}`

Delete a per-user spend limit override.

The member falls back to any inherited cap at that period. Seat-tier,
group, and organization-level rows cannot be deleted via this endpoint.

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
