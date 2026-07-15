---
source: platform
url: https://platform.claude.com/docs/en/api/admin/external_keys/delete
fetched_at: 2026-07-15T03:08:15.897796Z
sha256: 1fdae42af692219072cb029032a0ed10c62757f0c2ae6a25000fe18626f95538
---

## Delete External Key

**delete** `/v1/organizations/external_keys/{external_key_id}`

Delete an external key config.

The request is rejected if any workspace still references this config.

### Path Parameters

- `external_key_id: string`

  ID of the External Key.

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
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

#### Response

```json
{
  "id": "ekey_01AbCdEfGhIjKlMnOpQrStUv",
  "type": "external_key_deleted"
}
```
