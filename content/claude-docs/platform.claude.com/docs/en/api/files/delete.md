---
source: platform
url: https://platform.claude.com/docs/en/api/files/delete
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: b1fb42bf78020e0fb5be73c70ca270181d8ba52004ee806a874294dbb395570f
---

# Delete File

**DELETE** `/v1/files/{file_id}`

Delete File

## Path parameters

- `file_id: string`

  ID of the File.

## Returns

- `DeletedFile object`

  - `id: string`

    ID of the deleted file.

  - `type: optional "file_deleted"`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

    default: file_deleted

## Example

```bash
curl https://api.anthropic.com/v1/files/$FILE_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "type": "file_deleted"
}
```
