---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts/content
fetched_at: 2026-05-09T03:13:52.260309Z
sha256: 3a7b36b10dd493be87e9fb0517b400c3df85306b568b4a2770359b203924fb8a
---

## Content

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
