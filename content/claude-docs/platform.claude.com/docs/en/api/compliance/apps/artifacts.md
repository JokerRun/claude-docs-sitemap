---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts
fetched_at: 2026-05-09T03:13:52.260309Z
sha256: d195c94beb264896e7c0c0542dff9c6aebffd6c65287dca55959581d96ac9b4e
---

# Artifacts

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

## Domain Types

### Artifact Content Response

- `ArtifactContentResponse = unknown`
