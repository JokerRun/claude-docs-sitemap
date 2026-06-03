---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/projects/documents/delete
fetched_at: 2026-06-03T03:18:49.025048Z
sha256: 6b72ab613ca3c3322b54d56fccd41ebe54c9e41cab11104cf3bea6e5ba5fc419
---

## Delete project document

**delete** `/v1/compliance/apps/projects/documents/{document_id}`

Delete a project document for compliance purposes.

Hard-deletes the project document permanently.

### Path Parameters

- `document_id: string`

  The document ID (tagged ID, e.g., claude_proj_doc_abc123)

### Header Parameters

- `"x-api-key": optional string`

### Returns

- `id: string`

  The ID of the project document that was deleted

- `type: "claude_project_document_deleted"`

  Constant string confirming deletion.

  - `"claude_project_document_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/compliance/apps/projects/documents/$DOCUMENT_ID \
    -X DELETE \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

#### Response

```json
{
  "id": "id",
  "type": "claude_project_document_deleted"
}
```
