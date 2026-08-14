---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts/retrieve
fetched_at: 2026-08-14T02:57:38.618353Z
sha256: 3f79ab9ca3808aef720aea0258726a5aaa079c3516ee5485cf1e0554a85a92c4
---

---
title: Get artifact metadata
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts/retrieve
---

## Get artifact metadata

**get** `/v1/compliance/apps/artifacts/{artifact_version_id}`

Returns metadata for an artifact version, without the content body.

Use the sibling `/content` endpoint to fetch the artifact text. The
`md5` and `size_bytes` fields here are computed over the UTF-8
encoding of that text, so a DLP consumer can dedupe or match hashes
without downloading every artifact.

### Path Parameters

- `artifact_version_id: string`

  The artifact version ID (tagged ID, e.g., claude_artifact_version_abc123)

### Header Parameters

- `"x-api-key": optional string`

### Returns

- `id: string`

  Artifact ID e.g. 'claude_artifact_abc123'

- `artifact_type: string or null`

  MIME-like artifact type e.g. 'application/vnd.ant.code'

- `claude_chat_id: string`

  The chat this artifact belongs to

- `created_at: string`

  Artifact version creation timestamp

- `md5: string`

  Lowercase hex MD5 of the artifact content (UTF-8 encoded). Matches the `content` field returned by the sibling `/content` endpoint.

- `size_bytes: number`

  Size in bytes of the artifact content (UTF-8 encoded)

- `title: string or null`

  Artifact title

- `version_id: string`

  Artifact version ID e.g. 'claude_artifact_version_abc123'

### Example

```http
curl https://api.anthropic.com/v1/compliance/apps/artifacts/$ARTIFACT_VERSION_ID \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

#### Response

```json
{
  "id": "id",
  "artifact_type": "artifact_type",
  "claude_chat_id": "claude_chat_id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "md5": "md5",
  "size_bytes": 0,
  "title": "title",
  "version_id": "version_id"
}
```
