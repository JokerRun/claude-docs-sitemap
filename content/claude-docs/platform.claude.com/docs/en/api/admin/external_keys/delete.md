---
source: platform
url: https://platform.claude.com/docs/en/api/admin/external_keys/delete
fetched_at: 2026-06-02T03:18:54.775717Z
sha256: ee5c4f05083701a415539c5c5c45284123cdb820c927d8141d59272a90d88e9d
---

## Delete External Key

**delete** `/v1/organizations/external_keys/{external_key_id}`

Delete an external key config.

The request is rejected if any workspace still references this config.

### Path Parameters

- `external_key_id: string`

  ID of the External Key to delete.

### Returns

- `id: string`

  ID of the deleted External Key.

- `type: "external_key_deleted"`

  - `"external_key_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/external_keys/$EXTERNAL_KEY_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

#### Response

```json
{
  "id": "ekey_01AbCdEfGhIjKlMnOpQrStUv",
  "type": "external_key_deleted"
}
```
