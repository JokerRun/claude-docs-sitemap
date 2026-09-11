---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/rbac_groups/delete
fetched_at: 2026-09-11T02:21:44.680579Z
sha256: 023134a9cbc91581cc5d6f0885be0fe74fb50de55aed5f5a05d8b36d8616d736
---

---
title: Delete RBAC Group
url: https://platform.claude.com/docs/en/api/beta/organization/rbac_groups/delete
---

# Delete RBAC Group

**DELETE** `/v1/organizations/rbac_groups/{group_id}`

Delete an RBAC Group. Groups provisioned by an identity provider (source type `"scim"`) cannot be deleted via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Path parameters

- `group_id: string`

  ID of the RBAC Group.

## Returns

- `BetaRBACGroupDeleted object`

  - `type: "rbac_group_deleted"`

    Deleted object type.

    For RBAC Groups, this is always `"rbac_group_deleted"`.

    default: rbac_group_deleted

  - `id: string`

    ID of the RBAC Group.

## Example

```bash
curl https://api.anthropic.com/v1/organizations/rbac_groups/$GROUP_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H 'anthropic-beta: ce-user-management-2026-07-13' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_deleted"
}
```
