---
source: platform
url: https://platform.claude.com/docs/en/api/ruby/beta/webhooks/unwrap
fetched_at: 2026-05-06T03:14:02.071100Z
sha256: 3f3a3118ba6acb7122aeaf80edc2e0eb404a464536e7a7e410c904f576a925aa
---

## Unwrap

`beta.webhooks.unwrap() -> void`

**** ``

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

result = anthropic.beta.webhooks.unwrap

puts(result)
```
