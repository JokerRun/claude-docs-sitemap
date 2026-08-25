---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts/download
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: f722bcccd2e98bc632700eb1a91abcbff25927c98f0d7b607188d9be4f6f333e
---

# Download artifact content

**GET** `/v1/compliance/apps/artifacts/{artifact_version_id}/content`

Download the content of an artifact version for compliance purposes.

Returns the full text content of the artifact version.

## Path parameters

- `artifact_version_id: string`

  The artifact version ID (tagged ID, e.g., claude_artifact_version_abc123)

## Headers

- `"x-api-key": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/artifacts/$ARTIFACT_VERSION_ID/content \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
