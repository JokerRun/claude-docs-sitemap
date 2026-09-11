---
source: platform
url: https://platform.claude.com/docs/en/api/files/download
fetched_at: 2026-09-11T02:21:44.680579Z
sha256: 74f6c8470bd1d17c1aca6567430fd02f5f36de4451cad36117fff299a8bd1d1c
---

---
title: Download File
url: https://platform.claude.com/docs/en/api/files/download
---

# Download File

**GET** `/v1/files/{file_id}/content`

Download File

## Path parameters

- `file_id: string`

  ID of the File.

## Headers

- `"anthropic-workspace-id": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/files/$FILE_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```
