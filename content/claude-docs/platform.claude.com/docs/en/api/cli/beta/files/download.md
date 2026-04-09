---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/files/download
fetched_at: 2026-04-09T03:10:22.306859Z
sha256: c3f94484cd1c23d8c3b1b04dba6feef0e5b20c2acea8bcd4d43c5f26333c3cb0
---

## Download

`$ ant beta:files download`

**get** `/v1/files/{file_id}/content`

Download File

### Parameters

- `--file-id: string`

  ID of the File.

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `unnamed_schema_0: file path`

### Example

```cli
ant beta:files download \
  --api-key my-anthropic-api-key \
  --file-id file_id
```
