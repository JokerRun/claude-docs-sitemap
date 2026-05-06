---
source: platform
url: https://platform.claude.com/docs/en/api/go/beta/webhooks/unwrap
fetched_at: 2026-05-06T03:14:02.071100Z
sha256: 2945d25885dbda0c4c23c1416cc48fabc8ac7ef9e9d5540edb324894b03b43cb
---

## Unwrap

`client.Beta.Webhooks.Unwrap(ctx) error`

**** ``

### Example

```go
package main

import (
  "context"

  "github.com/anthropics/anthropic-sdk-go"
  "github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
  client := anthropic.NewClient(
    option.WithAPIKey("my-anthropic-api-key"),
  )
  err := client.Beta.Webhooks.Unwrap(context.TODO())
  if err != nil {
    panic(err.Error())
  }
}
```
