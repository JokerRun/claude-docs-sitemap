---
source: platform
url: https://platform.claude.com/docs/en/api/admin/workspaces/create
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: 2ae5612a3b90ba7e1d92af39fb63021bd961ee08ec2dcf253a09c3643ad15770
---

## Create

**post** `/v1/organizations/workspaces`

Create Workspace

### Body Parameters

- `name: string`

  Name of the Workspace.

- `data_residency: optional object { allowed_inference_geos, default_inference_geo, workspace_geo }`

  Data residency configuration for the workspace. If omitted, defaults to workspace_geo=`"us"`, allowed_inference_geos=`"unrestricted"`, and default_inference_geo=`"global"`.

  - `allowed_inference_geos: optional array of string or "unrestricted"`

    Permitted inference geo values. Defaults to 'unrestricted' if omitted, which allows all geos. Use the string 'unrestricted' to allow all geos, or a list of specific geos.

    - `UnionMember0 = array of string`

    - `UnionMember1 = "unrestricted"`

      - `"unrestricted"`

  - `default_inference_geo: optional string`

    Default inference geo applied when requests omit the parameter. Defaults to 'global' if omitted. Must be a member of allowed_inference_geos unless allowed_inference_geos is `"unrestricted"`.

  - `workspace_geo: optional string`

    Geographic region for workspace data storage. Immutable after creation. Defaults to 'us' if omitted.

### Returns

- `Workspace = object { id, archived_at, created_at, 4 more }`

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

  - `data_residency: object { allowed_inference_geos, default_inference_geo, workspace_geo }`

    Data residency configuration.

    - `allowed_inference_geos: array of string or "unrestricted"`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `UnionMember0 = array of string`

      - `UnionMember1 = "unrestricted"`

        - `"unrestricted"`

    - `default_inference_geo: string`

      Default inference geo applied when requests omit the parameter.

    - `workspace_geo: string`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `name: string`

    Name of the Workspace.

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

    - `"workspace"`
