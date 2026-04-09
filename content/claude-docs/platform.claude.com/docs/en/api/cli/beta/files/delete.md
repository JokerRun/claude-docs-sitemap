---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/files/delete
fetched_at: 2026-04-09T03:10:22.306859Z
sha256: c02f26c5212ae8da02ca65103c5d7888adce4950ce7cc1e87a53764b696d7854
---

## Delete

`$ ant beta:files delete`

**delete** `/v1/files/{file_id}`

Delete File

### Parameters

- `--file-id: string`

  ID of the File.

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `deleted_file: object { id, type }`

  - `id: string`

    ID of the deleted file.

  - `type: optional "file_deleted"`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

    - `"file_deleted"`

### Example

```cli
ant beta:files delete \
  --api-key my-anthropic-api-key \
  --file-id file_id
```
