---
source: platform
url: https://platform.claude.com/docs/en/api/admin/workspaces/members/create
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: be48bc1e3c5e927b93197412ab43cd8c2297039ebb2aa21550f22cdfd4a89fad
---

## Create

**post** `/v1/organizations/workspaces/{workspace_id}/members`

Create Workspace Member

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

### Body Parameters

- `user_id: string`

  ID of the User.

- `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin"`

  Role of the new Workspace Member. Cannot be "workspace_billing".

  - `"workspace_user"`

  - `"workspace_developer"`

  - `"workspace_admin"`

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
