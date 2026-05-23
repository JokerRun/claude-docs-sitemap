---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/files/download
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 5cc6cfa42787c2e53955358b6b4f5d3e1a950887fec6979a081d12c673f6c898
---

## Download File

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
