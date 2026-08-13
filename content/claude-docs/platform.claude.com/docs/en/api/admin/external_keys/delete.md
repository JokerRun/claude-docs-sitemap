---
source: platform
url: https://platform.claude.com/docs/en/api/admin/external_keys/delete
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: fde22d53154614dbc3bace1f5b6bd954235fa71c1aeeb640a04d7dd8f4f708bd
---

---
title: Delete External Key
url: https://platform.claude.com/docs/en/api/admin/external_keys/delete
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
