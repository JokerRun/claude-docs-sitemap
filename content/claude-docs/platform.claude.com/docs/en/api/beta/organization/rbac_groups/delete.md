---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/rbac_groups/delete
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 7196e789f14ce0d6d448f6b6334c496d6fbf010367df7b47c44838b594f9597a
---

---
title: Delete RBAC Group
url: https://platform.claude.com/docs/en/api/beta/organization/rbac_groups/delete
---

# Delete RBAC Group

**DELETE** `/v1/organizations/rbac_groups/{rbac_group_id}`

Delete an RBAC Group. Groups provisioned by an identity provider (source type `"scim"`) cannot be deleted via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Path parameters

- `rbac_group_id: string`

  ID of the RBAC Group.

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning).

## Returns

- `type: "rbac_group_deleted"`

  Deleted object type.

  For RBAC Groups, this is always `"rbac_group_deleted"`.

  default: rbac_group_deleted

- `id: string`

  ID of the RBAC Group.

## Example

```bash
curl https://api.anthropic.com/v1/organizations/rbac_groups/$RBAC_GROUP_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_deleted"
}
```
