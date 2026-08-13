---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/projects/documents/delete
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 53ba0eda8b3f6b2b90d49485b18f90f02d00a6a22ec1ec2c2c25c0c5deee8492
---

---
title: Delete project document
url: https://platform.claude.com/docs/en/api/compliance/apps/projects/documents/delete
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
