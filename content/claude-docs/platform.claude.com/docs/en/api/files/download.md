---
source: platform
url: https://platform.claude.com/docs/en/api/files/download
fetched_at: 2026-08-21T02:32:13.524433Z
sha256: 2569ebea7900321ac8c7fa63915d8ead7cc124d33aac3003ce9ae6ab4b514718
---

---
title: Download File
url: https://platform.claude.com/docs/en/api/files/download
---

## Download File

**get** `/v1/files/{file_id}/content`

Download File

### Path Parameters

- `file_id: string`

  ID of the File.

### Example

```http
curl https://api.anthropic.com/v1/files/$FILE_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```
