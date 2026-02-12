---
source: platform
url: https://platform.claude.com/docs/en/api/admin/workspaces/members/delete
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: 3717b10778895a9cd3831f94f08446361af830386ed8c48a0858b9dfc939a4bd
---

## Delete

**delete** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

- `user_id: string`

  ID of the User.

### Returns

- `type: "workspace_member_deleted"`

  Deleted object type.

  For Workspace Members, this is always `"workspace_member_deleted"`.

  - `"workspace_member_deleted"`

- `user_id: string`

  ID of the User.

- `workspace_id: string`

  ID of the Workspace.
