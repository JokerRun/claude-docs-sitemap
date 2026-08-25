---
source: platform
url: https://platform.claude.com/docs/en/api/admin/external_keys/delete
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: b42af66453b6cc472bb39e6d17bc44367f82fb371af5599f6c456bc31e0bea5a
---

# Delete External Key

**DELETE** `/v1/organizations/external_keys/{external_key_id}`

Delete an external key config.

The request is rejected if any workspace still references this config.

## Path parameters

- `external_key_id: string`

  ID of the External Key.

  maxLength: 2048

## Returns

- `id: string`

  ID of the deleted External Key.

- `type: "external_key_deleted"`

  default: external_key_deleted

## Example

```bash
curl https://api.anthropic.com/v1/organizations/external_keys/$EXTERNAL_KEY_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

### Response (200)

```json
{
  "id": "ekey_01AbCdEfGhIjKlMnOpQrStUv",
  "type": "external_key_deleted"
}
```
