---
source: platform
url: https://platform.claude.com/docs/en/api/files/download
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 01bc82427ee76635c85636fbe82e008bd153689b7ad6a756ae0eacf68bc56e66
---

# Download File

**GET** `/v1/files/{file_id}/content`

Download File

## Path parameters

- `file_id: string`

  ID of the File.

## Example

```bash
curl https://api.anthropic.com/v1/files/$FILE_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```
