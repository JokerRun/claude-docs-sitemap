---
source: platform
url: https://platform.claude.com/docs/en/api/organization/external_keys/delete
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 5ae749de7b2714b3f02473323ceefa685ac1a5168683307db26d3d7560ced043
---

---
title: Delete External Key
url: https://platform.claude.com/docs/en/api/organization/external_keys/delete
---

# Delete External Key

**DELETE** `/v1/organizations/external_keys/{external_key_id}`

Delete an external key config.

The request is rejected if any workspace still references this config.

## Path parameters

- `external_key_id: string`

  ID of the External Key.

  maxLength: 2048

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning).

## Returns

- `type: "external_key_deleted"`

  default: external_key_deleted

- `id: string`

  ID of the deleted External Key.

## Example

```bash
curl https://api.anthropic.com/v1/organizations/external_keys/$EXTERNAL_KEY_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "ekey_01AbCdEfGhIjKlMnOpQrStUv",
  "type": "external_key_deleted"
}
```
