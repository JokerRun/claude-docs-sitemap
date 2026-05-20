---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts/download
fetched_at: 2026-05-20T03:15:44.945478Z
sha256: f8a6a240fe87594b10308ca52cefc21bebcf22207cdaeec342e49eda7395b154
---

## Download

**get** `/v1/compliance/apps/artifacts/{artifact_version_id}/content`

Download the content of an artifact version for compliance purposes.

Returns the full text content of the artifact version.

### Path Parameters

- `artifact_version_id: string`

  The artifact version ID (tagged ID, e.g., claude_artifact_version_abc123)

### Header Parameters

- `"x-api-key": optional string`

### Example

```http
curl https://api.anthropic.com/v1/compliance/apps/artifacts/$ARTIFACT_VERSION_ID/content \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
