---
source: platform
url: https://platform.claude.com/docs/en/api/files/download
fetched_at: 2026-09-22T02:21:41.260167Z
sha256: aa100436d3b7a3b7a9bc349f823af9c65427360c9ecb0d1be22462bb3b4ef1cd
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

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Example

```bash
curl https://api.anthropic.com/v1/files/$FILE_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```
