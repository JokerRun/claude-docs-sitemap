---
source: platform
url: https://platform.claude.com/docs/en/api/admin/workspaces/members/update
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: 27028ebb7cf3e1c827cf4579c0c953ead89b1bb3fdadcea03a99fbca60d63ddd
---

## Update

**post** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Update Workspace Member

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

- `user_id: string`

  ID of the User.

### Body Parameters

- `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin" or "workspace_billing"`

  New workspace role for the User.

  - `"workspace_user"`

  - `"workspace_developer"`

  - `"workspace_admin"`

  - `"workspace_billing"`

### Returns

- `WorkspaceMember = object { type, user_id, workspace_id, workspace_role }`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    - `"workspace_member"`

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin" or "workspace_billing"`

    Role of the Workspace Member.

    - `"workspace_user"`

    - `"workspace_developer"`

    - `"workspace_admin"`

    - `"workspace_billing"`
