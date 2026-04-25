---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: 8e36c4de78252965b02889f732175013e3a792aab4aca32bdbfe775a9b70d81d
---

# Tutorial: Bangun agen yang menggunakan alat

Panduan langkah demi langkah dari satu panggilan alat hingga loop agentic yang siap produksi.

---

Tutorial ini membangun agen manajemen kalender dalam lima cincin konsentris. Setiap cincin adalah program lengkap yang dapat dijalankan dan menambahkan tepat satu konsep ke cincin sebelumnya. Di akhir, Anda akan telah menulis loop agentic dengan tangan dan kemudian menggantinya dengan abstraksi Tool Runner SDK.

Alat contoh adalah `create_calendar_event`. Skemanya menggunakan objek bersarang, array, dan bidang opsional, sehingga Anda akan melihat bagaimana Claude menangani bentuk input yang realistis daripada sekadar string datar tunggal.

<Note>
Setiap cincin berjalan mandiri. Salin cincin apa pun ke file baru dan itu akan dijalankan tanpa kode dari cincin sebelumnya.
</Note>

## Cincin 1: Satu alat, satu putaran

Program penggunaan alat terkecil yang mungkin: satu alat, satu pesan pengguna, satu panggilan alat, satu hasil. Kode diberi komentar berat sehingga Anda dapat memetakan setiap baris ke [siklus hidup penggunaan alat](/docs/id/agents-and-tools/tool-use/how-tool-use-works).

Permintaan mengirimkan array `tools` bersama pesan pengguna. Ketika Claude memutuskan untuk memanggil alat, respons kembali dengan `stop_reason: "tool_use"` dan blok konten `tool_use` yang berisi nama alat, `id` unik, dan `input` terstruktur. Kode Anda menjalankan alat, kemudian mengirimkan hasil kembali dalam blok `tool_result` yang `tool_use_id`-nya cocok dengan `id` dari panggilan.

<CodeGroup>
  
````bash
#!/bin/bash
# Ring 1: Single tool, single turn.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

# Define one tool as a JSON fragment. The input_schema is a JSON Schema
# object describing the arguments Claude should pass when it calls this
# tool. This schema includes nested objects (recurrence), arrays
# (attendees), and optional fields, which is closer to real-world tools
# than a flat string argument.
TOOLS='[
  {
    "name": "create_calendar_event",
    "description": "Create a calendar event with attendees and optional recurrence.",
    "input_schema": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "start": {"type": "string", "format": "date-time"},
        "end": {"type": "string", "format": "date-time"},
        "attendees": {
          "type": "array",
          "items": {"type": "string", "format": "email"}
        },
        "recurrence": {
          "type": "object",
          "properties": {
            "frequency": {"enum": ["daily", "weekly", "monthly"]},
            "count": {"type": "integer", "minimum": 1}
          }
        }
      },
      "required": ["title", "start", "end"]
    }
  }
]'

USER_MSG="Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am."

# Send the user's request along with the tool definition. Claude decides
# whether to call the tool based on the request and the tool description.
RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "$(jq -n \
    --argjson tools "$TOOLS" \
    --arg msg "$USER_MSG" \
    '{
      model: "claude-opus-4-6",
      max_tokens: 1024,
      tools: $tools,
      tool_choice: {type: "auto", disable_parallel_tool_use: true},
      messages: [{role: "user", content: $msg}]
    }')")

# When Claude calls a tool, the response has stop_reason "tool_use"
# and the content array contains a tool_use block alongside any text.
echo "stop_reason: $(echo "$RESPONSE" | jq -r '.stop_reason')"

# Find the tool_use block. A response may contain text blocks before the
# tool_use block, so filter by type rather than assuming position.
TOOL_USE=$(echo "$RESPONSE" | jq '.content[] | select(.type == "tool_use")')
TOOL_USE_ID=$(echo "$TOOL_USE" | jq -r '.id')
echo "Tool: $(echo "$TOOL_USE" | jq -r '.name')"
echo "Input: $(echo "$TOOL_USE" | jq -c '.input')"

# Execute the tool. In a real system this would call your calendar API.
# Here the result is hardcoded to keep the example self-contained.
RESULT='{"event_id": "evt_123", "status": "created"}'

# Send the result back. The tool_result block goes in a user message and
# its tool_use_id must match the id from the tool_use block above. The
# assistant's previous response is included so Claude has the full history.
ASSISTANT_CONTENT=$(echo "$RESPONSE" | jq '.content')
FOLLOWUP=$(curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "$(jq -n \
    --argjson tools "$TOOLS" \
    --arg msg "$USER_MSG" \
    --argjson assistant "$ASSISTANT_CONTENT" \
    --arg tool_use_id "$TOOL_USE_ID" \
    --arg result "$RESULT" \
    '{
      model: "claude-opus-4-6",
      max_tokens: 1024,
      tools: $tools,
      tool_choice: {type: "auto", disable_parallel_tool_use: true},
      messages: [
        {role: "user", content: $msg},
        {role: "assistant", content: $assistant},
        {role: "user", content: [
          {type: "tool_result", tool_use_id: $tool_use_id, content: $result}
        ]}
      ]
    }')")

# With the tool result in hand, Claude produces a final natural-language
# answer and stop_reason becomes "end_turn".
echo "stop_reason: $(echo "$FOLLOWUP" | jq -r '.stop_reason')"
echo "$FOLLOWUP" | jq -r '.content[] | select(.type == "text") | .text'
````

  
````bash
#!/usr/bin/env bash
# Ring 1: Single tool, single turn.
# Uses jq for cross-turn message-array state — building an agentic loop in shell
# requires JSON manipulation beyond ant's single-call --transform scope.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.
set -euo pipefail

USER_MSG="Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am."
MESSAGES=$(jq -n --arg msg "$USER_MSG" '[{role: "user", content: $msg}]')

# Define one tool. The input_schema is a JSON Schema object describing
# the arguments Claude should pass when it calls this tool. This schema
# includes nested objects (recurrence), arrays (attendees), and optional
# fields, which is closer to real-world tools than a flat string argument.
call_api() {
  # ant reads the request body as YAML on stdin: no auth headers, no
  # hand-built JSON envelope. The static keys (model, tools, tool_choice)
  # live in a quoted heredoc; the growing messages array is appended as
  # JSON, which YAML accepts as flow syntax.
  {
    cat <<'YAML'
model: claude-opus-4-6
max_tokens: 1024
tool_choice: {type: auto, disable_parallel_tool_use: true}
tools:
  - name: create_calendar_event
    description: Create a calendar event with attendees and optional recurrence.
    input_schema:
      type: object
      properties:
        title: {type: string}
        start: {type: string, format: date-time}
        end: {type: string, format: date-time}
        attendees:
          type: array
          items: {type: string, format: email}
        recurrence:
          type: object
          properties:
            frequency: {enum: [daily, weekly, monthly]}
            count: {type: integer, minimum: 1}
      required: [title, start, end]
YAML
    printf 'messages: %s\n' "$MESSAGES"
  } | ant messages create --format json
}

# Send the user's request along with the tool definition. Claude decides
# whether to call the tool based on the request and the tool description.
RESPONSE=$(call_api)

# When Claude calls a tool, the response has stop_reason "tool_use"
# and the content array contains a tool_use block alongside any text.
echo "stop_reason: $(jq -r '.stop_reason' <<<"$RESPONSE")"

# Find the tool_use block. A response may contain text blocks before the
# tool_use block, so filter by type rather than assuming position.
TOOL_USE=$(jq '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")
TOOL_USE_ID=$(jq -r '.id' <<<"$TOOL_USE")
echo "Tool: $(jq -r '.name' <<<"$TOOL_USE")"
echo "Input: $(jq -c '.input' <<<"$TOOL_USE")"

# Execute the tool. In a real system this would call your calendar API.
# Here the result is hardcoded to keep the example self-contained.
RESULT='{"event_id": "evt_123", "status": "created"}'

# Send the result back. The tool_result block goes in a user message and
# its tool_use_id must match the id from the tool_use block above. The
# assistant's previous response is included so Claude has the full history.
MESSAGES=$(jq \
  --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
  --arg tool_use_id "$TOOL_USE_ID" \
  --arg result "$RESULT" \
  '. + [
    {role: "assistant", content: $assistant},
    {role: "user", content: [
      {type: "tool_result", tool_use_id: $tool_use_id, content: $result}
    ]}
  ]' <<<"$MESSAGES")

FOLLOWUP=$(call_api)

# With the tool result in hand, Claude produces a final natural-language
# answer and stop_reason becomes "end_turn".
echo "stop_reason: $(jq -r '.stop_reason' <<<"$FOLLOWUP")"
jq -r '.content[] | select(.type == "text") | .text' <<<"$FOLLOWUP"
````

  
````python
# Ring 1: Single tool, single turn.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

import json

import anthropic

# Create a client. It reads ANTHROPIC_API_KEY from the environment.
client = anthropic.Anthropic()

# Define one tool. The input_schema is a JSON Schema object describing
# the arguments Claude should pass when it calls this tool. This schema
# includes nested objects (recurrence), arrays (attendees), and optional
# fields, which is closer to real-world tools than a flat string argument.
tools = [
    {
        "name": "create_calendar_event",
        "description": "Create a calendar event with attendees and optional recurrence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "start": {"type": "string", "format": "date-time"},
                "end": {"type": "string", "format": "date-time"},
                "attendees": {
                    "type": "array",
                    "items": {"type": "string", "format": "email"},
                },
                "recurrence": {
                    "type": "object",
                    "properties": {
                        "frequency": {"enum": ["daily", "weekly", "monthly"]},
                        "count": {"type": "integer", "minimum": 1},
                    },
                },
            },
            "required": ["title", "start", "end"],
        },
    }
]

# Send the user's request along with the tool definition. Claude decides
# whether to call the tool based on the request and the tool description.
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto", "disable_parallel_tool_use": True},
    messages=[
        {
            "role": "user",
            "content": "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am.",
        }
    ],
)

# When Claude calls a tool, the response has stop_reason "tool_use"
# and the content array contains a tool_use block alongside any text.
print(f"stop_reason: {response.stop_reason}")

# Find the tool_use block. A response may contain text blocks before the
# tool_use block, so scan the content array rather than assuming position.
tool_use = next(block for block in response.content if block.type == "tool_use")
print(f"Tool: {tool_use.name}")
print(f"Input: {tool_use.input}")

# Execute the tool. In a real system this would call your calendar API.
# Here the result is hardcoded to keep the example self-contained.
result = {"event_id": "evt_123", "status": "created"}

# Send the result back. The tool_result block goes in a user message and
# its tool_use_id must match the id from the tool_use block above. The
# assistant's previous response is included so Claude has the full history.
followup = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto", "disable_parallel_tool_use": True},
    messages=[
        {
            "role": "user",
            "content": "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am.",
        },
        {"role": "assistant", "content": response.content},
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result),
                }
            ],
        },
    ],
)

# With the tool result in hand, Claude produces a final natural-language
# answer and stop_reason becomes "end_turn".
print(f"stop_reason: {followup.stop_reason}")
final_text = next(block for block in followup.content if block.type == "text")
print(final_text.text)
````

  
````typescript
// Ring 1: Single tool, single turn.
// Source for <CodeSource> in build-a-tool-using-agent.mdx.

import Anthropic from "@anthropic-ai/sdk";

// Create a client. It reads ANTHROPIC_API_KEY from the environment.
const client = new Anthropic();

// Define one tool. The input_schema is a JSON Schema object describing
// the arguments Claude should pass when it calls this tool. This schema
// includes nested objects (recurrence), arrays (attendees), and optional
// fields, which is closer to real-world tools than a flat string argument.
const tools: Anthropic.Tool[] = [
  {
    name: "create_calendar_event",
    description:
      "Create a calendar event with attendees and optional recurrence.",
    input_schema: {
      type: "object",
      properties: {
        title: { type: "string" },
        start: { type: "string", format: "date-time" },
        end: { type: "string", format: "date-time" },
        attendees: {
          type: "array",
          items: { type: "string", format: "email" },
        },
        recurrence: {
          type: "object",
          properties: {
            frequency: { enum: ["daily", "weekly", "monthly"] },
            count: { type: "integer", minimum: 1 },
          },
        },
      },
      required: ["title", "start", "end"],
    },
  },
];

// Send the user's request along with the tool definition. Claude decides
// whether to call the tool based on the request and the tool description.
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools,
  tool_choice: { type: "auto", disable_parallel_tool_use: true },
  messages: [
    {
      role: "user",
      content:
        "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am.",
    },
  ],
});

// When Claude calls a tool, the response has stop_reason "tool_use"
// and the content array contains a tool_use block alongside any text.
console.log(`stop_reason: ${response.stop_reason}`);

// Find the tool_use block. A response may contain text blocks before the
// tool_use block, so scan the content array rather than assuming position.
const toolUse = response.content.find(
  (block): block is Anthropic.ToolUseBlock => block.type === "tool_use",
)!;
console.log(`Tool: ${toolUse.name}`);
console.log(`Input: ${JSON.stringify(toolUse.input)}`);

// Execute the tool. In a real system this would call your calendar API.
// Here the result is hardcoded to keep the example self-contained.
const result = { event_id: "evt_123", status: "created" };

// Send the result back. The tool_result block goes in a user message and
// its tool_use_id must match the id from the tool_use block above. The
// assistant's previous response is included so Claude has the full history.
const followup = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools,
  tool_choice: { type: "auto", disable_parallel_tool_use: true },
  messages: [
    {
      role: "user",
      content:
        "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am.",
    },
    { role: "assistant", content: response.content },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: toolUse.id,
          content: JSON.stringify(result),
        },
      ],
    },
  ],
});

// With the tool result in hand, Claude produces a final natural-language
// answer and stop_reason becomes "end_turn".
console.log(`stop_reason: ${followup.stop_reason}`);
for (const block of followup.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
````

</CodeGroup>

**Apa yang diharapkan**

```text Output
stop_reason: tool_use
Tool: create_calendar_event
Input: {'title': 'Sync', 'start': '2026-03-30T10:00:00', 'end': '2026-03-30T10:30:00', 'attendees': ['alice@example.com', 'bob@example.com']}
stop_reason: end_turn
I've scheduled your 30-minute sync with Alice and Bob for next Monday at 10am.
```

`stop_reason` pertama adalah `tool_use` karena Claude menunggu hasil kalender. Setelah Anda mengirimkan hasil, `stop_reason` kedua adalah `end_turn` dan kontennya adalah bahasa alami untuk pengguna.

## Cincin 2: Loop agentic

Cincin 1 mengasumsikan Claude akan memanggil alat tepat satu kali. Tugas nyata sering memerlukan beberapa panggilan: Claude mungkin membuat acara, membaca konfirmasi, kemudian membuat yang lain. Solusinya adalah loop `while` yang terus menjalankan alat dan memberi umpan balik hasil hingga `stop_reason` tidak lagi `"tool_use"`.

Perubahan lainnya adalah riwayat percakapan. Alih-alih membangun kembali array `messages` dari awal pada setiap permintaan, simpan daftar yang berjalan dan tambahkan ke dalamnya. Setiap putaran melihat konteks sebelumnya yang lengkap.

<CodeGroup>
  
````bash
#!/bin/bash
# Ring 2: The agentic loop.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

TOOLS='[
  {
    "name": "create_calendar_event",
    "description": "Create a calendar event with attendees and optional recurrence.",
    "input_schema": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "start": {"type": "string", "format": "date-time"},
        "end": {"type": "string", "format": "date-time"},
        "attendees": {"type": "array", "items": {"type": "string", "format": "email"}},
        "recurrence": {
          "type": "object",
          "properties": {
            "frequency": {"enum": ["daily", "weekly", "monthly"]},
            "count": {"type": "integer", "minimum": 1}
          }
        }
      },
      "required": ["title", "start", "end"]
    }
  }
]'

run_tool() {
  local name="$1"
  local input="$2"
  if [ "$name" = "create_calendar_event" ]; then
    local title=$(echo "$input" | jq -r '.title')
    jq -n --arg title "$title" '{event_id: "evt_123", status: "created", title: $title}'
  else
    echo "{\"error\": \"Unknown tool: $name\"}"
  fi
}

# Keep the full conversation history in a JSON array so each turn sees prior context.
MESSAGES='[{"role": "user", "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."}]'

call_api() {
  curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n --argjson tools "$TOOLS" --argjson messages "$MESSAGES" \
      '{model: "claude-opus-4-6", max_tokens: 1024, tools: $tools, tool_choice: {type: "auto", disable_parallel_tool_use: true}, messages: $messages}')"
}

RESPONSE=$(call_api)

# Loop until Claude stops asking for tools. Each iteration runs the requested
# tool, appends the result to history, and asks Claude to continue.
while [ "$(echo "$RESPONSE" | jq -r '.stop_reason')" = "tool_use" ]; do
  TOOL_USE=$(echo "$RESPONSE" | jq '.content[] | select(.type == "tool_use")')
  TOOL_NAME=$(echo "$TOOL_USE" | jq -r '.name')
  TOOL_INPUT=$(echo "$TOOL_USE" | jq -c '.input')
  TOOL_USE_ID=$(echo "$TOOL_USE" | jq -r '.id')
  RESULT=$(run_tool "$TOOL_NAME" "$TOOL_INPUT")

  ASSISTANT_CONTENT=$(echo "$RESPONSE" | jq '.content')
  MESSAGES=$(echo "$MESSAGES" | jq \
    --argjson assistant "$ASSISTANT_CONTENT" \
    --arg tool_use_id "$TOOL_USE_ID" \
    --arg result "$RESULT" \
    '. + [
      {role: "assistant", content: $assistant},
      {role: "user", content: [{type: "tool_result", tool_use_id: $tool_use_id, content: $result}]}
    ]')

  RESPONSE=$(call_api)
done

echo "$RESPONSE" | jq -r '.content[] | select(.type == "text") | .text'
````

  
````bash
#!/usr/bin/env bash
# Ring 2: The agentic loop.
# Uses jq for cross-turn message-array state — building an agentic loop in shell
# requires JSON manipulation beyond ant's single-call --transform scope.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.
set -euo pipefail

run_tool() {
  local name="$1" input="$2"
  if [ "$name" = "create_calendar_event" ]; then
    jq -n --arg title "$(jq -r '.title' <<<"$input")" \
      '{event_id: "evt_123", status: "created", title: $title}'
  else
    printf '{"error": "Unknown tool: %s"}' "$name"
  fi
}

# Keep the full conversation history in a JSON array so each turn sees
# prior context.
MESSAGES='[{"role": "user", "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."}]'

call_api() {
  # ant reads the request body as YAML on stdin: no auth headers, no
  # hand-built JSON envelope. The static keys (model, tools, tool_choice)
  # live in a quoted heredoc; the growing messages array is appended as
  # JSON, which YAML accepts as flow syntax.
  {
    cat <<'YAML'
model: claude-opus-4-6
max_tokens: 1024
tool_choice: {type: auto, disable_parallel_tool_use: true}
tools:
  - name: create_calendar_event
    description: Create a calendar event with attendees and optional recurrence.
    input_schema:
      type: object
      properties:
        title: {type: string}
        start: {type: string, format: date-time}
        end: {type: string, format: date-time}
        attendees:
          type: array
          items: {type: string, format: email}
        recurrence:
          type: object
          properties:
            frequency: {enum: [daily, weekly, monthly]}
            count: {type: integer, minimum: 1}
      required: [title, start, end]
YAML
    printf 'messages: %s\n' "$MESSAGES"
  } | ant messages create --format json
}

RESPONSE=$(call_api)

# Loop until Claude stops asking for tools. Each iteration runs the
# requested tool, appends the result to history, and asks Claude to
# continue.
while [ "$(jq -r '.stop_reason' <<<"$RESPONSE")" = "tool_use" ]; do
  TOOL_USE=$(jq '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")
  TOOL_NAME=$(jq -r '.name' <<<"$TOOL_USE")
  TOOL_INPUT=$(jq -c '.input' <<<"$TOOL_USE")
  TOOL_USE_ID=$(jq -r '.id' <<<"$TOOL_USE")
  RESULT=$(run_tool "$TOOL_NAME" "$TOOL_INPUT")

  MESSAGES=$(jq \
    --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
    --arg tool_use_id "$TOOL_USE_ID" \
    --arg result "$RESULT" \
    '. + [
      {role: "assistant", content: $assistant},
      {role: "user", content: [
        {type: "tool_result", tool_use_id: $tool_use_id, content: $result}
      ]}
    ]' <<<"$MESSAGES")

  RESPONSE=$(call_api)
done

jq -r '.content[] | select(.type == "text") | .text' <<<"$RESPONSE"
````

  
````python
# Ring 2: The agentic loop.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

import json

import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "create_calendar_event",
        "description": "Create a calendar event with attendees and optional recurrence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "start": {"type": "string", "format": "date-time"},
                "end": {"type": "string", "format": "date-time"},
                "attendees": {
                    "type": "array",
                    "items": {"type": "string", "format": "email"},
                },
                "recurrence": {
                    "type": "object",
                    "properties": {
                        "frequency": {"enum": ["daily", "weekly", "monthly"]},
                        "count": {"type": "integer", "minimum": 1},
                    },
                },
            },
            "required": ["title", "start", "end"],
        },
    }
]


def run_tool(name, tool_input):
    if name == "create_calendar_event":
        return {"event_id": "evt_123", "status": "created", "title": tool_input["title"]}
    return {"error": f"Unknown tool: {name}"}


# Keep the full conversation history in a list so each turn sees prior context.
messages = [
    {
        "role": "user",
        "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
    }
]

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto", "disable_parallel_tool_use": True},
    messages=messages,
)

# Loop until Claude stops asking for tools. Each iteration runs the requested
# tool, appends the result to history, and asks Claude to continue.
while response.stop_reason == "tool_use":
    tool_use = next(block for block in response.content if block.type == "tool_use")
    result = run_tool(tool_use.name, tool_use.input)

    messages.append({"role": "assistant", "content": response.content})
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result),
                }
            ],
        }
    )

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        messages=messages,
    )

final_text = next(block for block in response.content if block.type == "text")
print(final_text.text)
````

  
````typescript
// Ring 2: The agentic loop.
// Source for <CodeSource> in build-a-tool-using-agent.mdx.

import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
  {
    name: "create_calendar_event",
    description:
      "Create a calendar event with attendees and optional recurrence.",
    input_schema: {
      type: "object",
      properties: {
        title: { type: "string" },
        start: { type: "string", format: "date-time" },
        end: { type: "string", format: "date-time" },
        attendees: {
          type: "array",
          items: { type: "string", format: "email" },
        },
        recurrence: {
          type: "object",
          properties: {
            frequency: { enum: ["daily", "weekly", "monthly"] },
            count: { type: "integer", minimum: 1 },
          },
        },
      },
      required: ["title", "start", "end"],
    },
  },
];

function runTool(name: string, input: Record<string, unknown>) {
  if (name === "create_calendar_event") {
    return { event_id: "evt_123", status: "created", title: input.title };
  }
  return { error: `Unknown tool: ${name}` };
}

// Keep the full conversation history so each turn sees prior context.
const messages: Anthropic.MessageParam[] = [
  {
    role: "user",
    content:
      "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
  },
];

let response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools,
  tool_choice: { type: "auto", disable_parallel_tool_use: true },
  messages,
});

// Loop until Claude stops asking for tools. Each iteration runs the requested
// tool, appends the result to history, and asks Claude to continue.
while (response.stop_reason === "tool_use") {
  const toolUse = response.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === "tool_use",
  )!;
  const result = runTool(toolUse.name, toolUse.input as Record<string, unknown>);

  messages.push({ role: "assistant", content: response.content });
  messages.push({
    role: "user",
    content: [
      {
        type: "tool_result",
        tool_use_id: toolUse.id,
        content: JSON.stringify(result),
      },
    ],
  });

  response = await client.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 1024,
    tools,
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages,
  });
}

for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
````

</CodeGroup>

**Apa yang diharapkan**

```text Output
I've set up your weekly team standup for the next 4 Mondays at 9am with Alice, Bob, and Carol invited.
```

Loop dapat berjalan sekali atau beberapa kali tergantung pada bagaimana Claude memecah tugas. Kode Anda tidak perlu lagi mengetahui sebelumnya.

## Cincin 3: Beberapa alat, panggilan paralel

Agen jarang memiliki hanya satu kemampuan. Tambahkan alat kedua, `list_calendar_events`, sehingga Claude dapat memeriksa jadwal yang ada sebelum membuat sesuatu yang baru.

Ketika Claude memiliki beberapa panggilan alat independen untuk dibuat, itu dapat mengembalikan beberapa blok `tool_use` dalam satu respons. Loop Anda perlu memproses semuanya dan mengirimkan semua hasil bersama-sama dalam satu pesan pengguna. Ulangi setiap blok `tool_use` dalam `response.content`, bukan hanya yang pertama.

<CodeGroup>
  
````bash
#!/bin/bash
# Ring 3: Multiple tools, parallel calls.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

TOOLS='[
  {
    "name": "create_calendar_event",
    "description": "Create a calendar event with attendees and optional recurrence.",
    "input_schema": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "start": {"type": "string", "format": "date-time"},
        "end": {"type": "string", "format": "date-time"},
        "attendees": {"type": "array", "items": {"type": "string", "format": "email"}},
        "recurrence": {
          "type": "object",
          "properties": {
            "frequency": {"enum": ["daily", "weekly", "monthly"]},
            "count": {"type": "integer", "minimum": 1}
          }
        }
      },
      "required": ["title", "start", "end"]
    }
  },
  {
    "name": "list_calendar_events",
    "description": "List all calendar events on a given date.",
    "input_schema": {
      "type": "object",
      "properties": {"date": {"type": "string", "format": "date"}},
      "required": ["date"]
    }
  }
]'

run_tool() {
  case "$1" in
    create_calendar_event)
      jq -n --arg title "$(echo "$2" | jq -r '.title')" '{event_id: "evt_123", status: "created", title: $title}' ;;
    list_calendar_events)
      echo '{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}' ;;
    *)
      echo "{\"error\": \"Unknown tool: $1\"}" ;;
  esac
}

MESSAGES='[{"role": "user", "content": "Check what I have next Monday, then schedule a planning session that avoids any conflicts."}]'

call_api() {
  curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n --argjson tools "$TOOLS" --argjson messages "$MESSAGES" \
      '{model: "claude-opus-4-6", max_tokens: 1024, tools: $tools, messages: $messages}')"
}

RESPONSE=$(call_api)

while [ "$(echo "$RESPONSE" | jq -r '.stop_reason')" = "tool_use" ]; do
  # A single response can contain multiple tool_use blocks. Process all of
  # them and return all results together in one user message.
  TOOL_RESULTS='[]'
  while read -r block; do
    NAME=$(echo "$block" | jq -r '.name')
    INPUT=$(echo "$block" | jq -c '.input')
    ID=$(echo "$block" | jq -r '.id')
    RESULT=$(run_tool "$NAME" "$INPUT")
    TOOL_RESULTS=$(echo "$TOOL_RESULTS" | jq --arg id "$ID" --arg result "$RESULT" \
      '. + [{type: "tool_result", tool_use_id: $id, content: $result}]')
  done < <(echo "$RESPONSE" | jq -c '.content[] | select(.type == "tool_use")')

  MESSAGES=$(echo "$MESSAGES" | jq \
    --argjson assistant "$(echo "$RESPONSE" | jq '.content')" \
    --argjson results "$TOOL_RESULTS" \
    '. + [{role: "assistant", content: $assistant}, {role: "user", content: $results}]')

  RESPONSE=$(call_api)
done

echo "$RESPONSE" | jq -r '.content[] | select(.type == "text") | .text'
````

  
````bash
#!/usr/bin/env bash
# Ring 3: Multiple tools, parallel calls.
# Uses jq for cross-turn message-array state — building an agentic loop in shell
# requires JSON manipulation beyond ant's single-call --transform scope.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.
set -euo pipefail

run_tool() {
  case "$1" in
    create_calendar_event)
      jq -n --arg title "$(jq -r '.title' <<<"$2")" \
        '{event_id: "evt_123", status: "created", title: $title}' ;;
    list_calendar_events)
      echo '{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}' ;;
    *)
      printf '{"error": "Unknown tool: %s"}' "$1" ;;
  esac
}

MESSAGES='[{"role": "user", "content": "Check what I have next Monday, then schedule a planning session that avoids any conflicts."}]'

call_api() {
  # ant reads the request body as YAML on stdin: no auth headers, no
  # hand-built JSON envelope. The static keys (model, tools) live in a
  # quoted heredoc; the growing messages array is appended as JSON,
  # which YAML accepts as flow syntax.
  {
    cat <<'YAML'
model: claude-opus-4-6
max_tokens: 1024
tools:
  - name: create_calendar_event
    description: Create a calendar event with attendees and optional recurrence.
    input_schema:
      type: object
      properties:
        title: {type: string}
        start: {type: string, format: date-time}
        end: {type: string, format: date-time}
        attendees:
          type: array
          items: {type: string, format: email}
        recurrence:
          type: object
          properties:
            frequency: {enum: [daily, weekly, monthly]}
            count: {type: integer, minimum: 1}
      required: [title, start, end]
  - name: list_calendar_events
    description: List all calendar events on a given date.
    input_schema:
      type: object
      properties:
        date: {type: string, format: date}
      required: [date]
YAML
    printf 'messages: %s\n' "$MESSAGES"
  } | ant messages create --format json
}

RESPONSE=$(call_api)

while [ "$(jq -r '.stop_reason' <<<"$RESPONSE")" = "tool_use" ]; do
  # A single response can contain multiple tool_use blocks. Process all
  # of them and return all results together in one user message.
  TOOL_RESULTS='[]'
  while read -r block; do
    NAME=$(jq -r '.name' <<<"$block")
    INPUT=$(jq -c '.input' <<<"$block")
    ID=$(jq -r '.id' <<<"$block")
    RESULT=$(run_tool "$NAME" "$INPUT")
    TOOL_RESULTS=$(jq --arg id "$ID" --arg result "$RESULT" \
      '. + [{type: "tool_result", tool_use_id: $id, content: $result}]' \
      <<<"$TOOL_RESULTS")
  done < <(jq -c '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")

  MESSAGES=$(jq \
    --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
    --argjson results "$TOOL_RESULTS" \
    '. + [
      {role: "assistant", content: $assistant},
      {role: "user", content: $results}
    ]' <<<"$MESSAGES")

  RESPONSE=$(call_api)
done

jq -r '.content[] | select(.type == "text") | .text' <<<"$RESPONSE"
````

  
````python
# Ring 3: Multiple tools, parallel calls.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

import json

import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "create_calendar_event",
        "description": "Create a calendar event with attendees and optional recurrence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "start": {"type": "string", "format": "date-time"},
                "end": {"type": "string", "format": "date-time"},
                "attendees": {
                    "type": "array",
                    "items": {"type": "string", "format": "email"},
                },
                "recurrence": {
                    "type": "object",
                    "properties": {
                        "frequency": {"enum": ["daily", "weekly", "monthly"]},
                        "count": {"type": "integer", "minimum": 1},
                    },
                },
            },
            "required": ["title", "start", "end"],
        },
    },
    {
        "name": "list_calendar_events",
        "description": "List all calendar events on a given date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "format": "date"},
            },
            "required": ["date"],
        },
    },
]


def run_tool(name, tool_input):
    if name == "create_calendar_event":
        return {"event_id": "evt_123", "status": "created", "title": tool_input["title"]}
    if name == "list_calendar_events":
        return {"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}
    return {"error": f"Unknown tool: {name}"}


messages = [
    {
        "role": "user",
        "content": "Check what I have next Monday, then schedule a planning session that avoids any conflicts.",
    }
]

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

while response.stop_reason == "tool_use":
    # A single response can contain multiple tool_use blocks. Process all of
    # them and return all results together in one user message.
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = run_tool(block.name, block.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                }
            )

    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

final_text = next(block for block in response.content if block.type == "text")
print(final_text.text)
````

  
````typescript
// Ring 3: Multiple tools, parallel calls.
// Source for <CodeSource> in build-a-tool-using-agent.mdx.

import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
  {
    name: "create_calendar_event",
    description:
      "Create a calendar event with attendees and optional recurrence.",
    input_schema: {
      type: "object",
      properties: {
        title: { type: "string" },
        start: { type: "string", format: "date-time" },
        end: { type: "string", format: "date-time" },
        attendees: {
          type: "array",
          items: { type: "string", format: "email" },
        },
        recurrence: {
          type: "object",
          properties: {
            frequency: { enum: ["daily", "weekly", "monthly"] },
            count: { type: "integer", minimum: 1 },
          },
        },
      },
      required: ["title", "start", "end"],
    },
  },
  {
    name: "list_calendar_events",
    description: "List all calendar events on a given date.",
    input_schema: {
      type: "object",
      properties: {
        date: { type: "string", format: "date" },
      },
      required: ["date"],
    },
  },
];

function runTool(name: string, input: Record<string, unknown>) {
  if (name === "create_calendar_event") {
    return { event_id: "evt_123", status: "created", title: input.title };
  }
  if (name === "list_calendar_events") {
    return {
      events: [{ title: "Existing meeting", start: "14:00", end: "15:00" }],
    };
  }
  return { error: `Unknown tool: ${name}` };
}

const messages: Anthropic.MessageParam[] = [
  {
    role: "user",
    content:
      "Check what I have next Monday, then schedule a planning session that avoids any conflicts.",
  },
];

let response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools,
  messages,
});

while (response.stop_reason === "tool_use") {
  // A single response can contain multiple tool_use blocks. Process all of
  // them and return all results together in one user message.
  const toolResults: Anthropic.ToolResultBlockParam[] = [];
  for (const block of response.content) {
    if (block.type === "tool_use") {
      const result = runTool(block.name, block.input as Record<string, unknown>);
      toolResults.push({
        type: "tool_result",
        tool_use_id: block.id,
        content: JSON.stringify(result),
      });
    }
  }

  messages.push({ role: "assistant", content: response.content });
  messages.push({ role: "user", content: toolResults });

  response = await client.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 1024,
    tools,
    messages,
  });
}

for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
````

</CodeGroup>

**Apa yang diharapkan**

```text Output
I checked your calendar for next Monday and found an existing meeting from 2pm to 3pm. I've scheduled the planning session for 10am to 11am to avoid the conflict.
```

Untuk informasi lebih lanjut tentang eksekusi bersamaan dan jaminan pengurutan, lihat [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use).

## Cincin 4: Penanganan kesalahan

Alat gagal. API kalender mungkin menolak acara dengan terlalu banyak peserta, atau tanggal mungkin salah format. Ketika alat memunculkan kesalahan, kirimkan pesan kesalahan kembali dengan `is_error: true` alih-alih mogok. Claude membaca kesalahan dan dapat mencoba lagi dengan input yang diperbaiki, meminta klarifikasi dari pengguna, atau menjelaskan keterbatasan.

<CodeGroup>
  
````bash
#!/bin/bash
# Ring 4: Error handling.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

TOOLS='[
  {
    "name": "create_calendar_event",
    "description": "Create a calendar event with attendees and optional recurrence.",
    "input_schema": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "start": {"type": "string", "format": "date-time"},
        "end": {"type": "string", "format": "date-time"},
        "attendees": {"type": "array", "items": {"type": "string", "format": "email"}},
        "recurrence": {
          "type": "object",
          "properties": {
            "frequency": {"enum": ["daily", "weekly", "monthly"]},
            "count": {"type": "integer", "minimum": 1}
          }
        }
      },
      "required": ["title", "start", "end"]
    }
  },
  {
    "name": "list_calendar_events",
    "description": "List all calendar events on a given date.",
    "input_schema": {
      "type": "object",
      "properties": {"date": {"type": "string", "format": "date"}},
      "required": ["date"]
    }
  }
]'

run_tool() {
  case "$1" in
    create_calendar_event)
      local count=$(echo "$2" | jq '.attendees | length // 0')
      if [ "$count" -gt 10 ]; then
        echo "ERROR: Too many attendees (max 10)"
        return 1
      fi
      jq -n --arg title "$(echo "$2" | jq -r '.title')" '{event_id: "evt_123", status: "created", title: $title}' ;;
    list_calendar_events)
      echo '{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}' ;;
    *)
      echo "ERROR: Unknown tool: $1"
      return 1 ;;
  esac
}

EMAILS=$(seq 0 14 | sed 's/.*/user&@example.com/' | paste -sd, -)
MESSAGES="[{\"role\": \"user\", \"content\": \"Schedule an all-hands with everyone: $EMAILS\"}]"

call_api() {
  curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n --argjson tools "$TOOLS" --argjson messages "$MESSAGES" \
      '{model: "claude-opus-4-6", max_tokens: 1024, tools: $tools, messages: $messages}')"
}

RESPONSE=$(call_api)

while [ "$(echo "$RESPONSE" | jq -r '.stop_reason')" = "tool_use" ]; do
  TOOL_RESULTS='[]'
  while read -r block; do
    NAME=$(echo "$block" | jq -r '.name')
    INPUT=$(echo "$block" | jq -c '.input')
    ID=$(echo "$block" | jq -r '.id')
    if OUTPUT=$(run_tool "$NAME" "$INPUT"); then
      TOOL_RESULTS=$(echo "$TOOL_RESULTS" | jq --arg id "$ID" --arg result "$OUTPUT" \
        '. + [{type: "tool_result", tool_use_id: $id, content: $result}]')
    else
      # Signal failure so Claude can retry or ask for clarification.
      TOOL_RESULTS=$(echo "$TOOL_RESULTS" | jq --arg id "$ID" --arg result "$OUTPUT" \
        '. + [{type: "tool_result", tool_use_id: $id, content: $result, is_error: true}]')
    fi
  done < <(echo "$RESPONSE" | jq -c '.content[] | select(.type == "tool_use")')

  MESSAGES=$(echo "$MESSAGES" | jq \
    --argjson assistant "$(echo "$RESPONSE" | jq '.content')" \
    --argjson results "$TOOL_RESULTS" \
    '. + [{role: "assistant", content: $assistant}, {role: "user", content: $results}]')

  RESPONSE=$(call_api)
done

echo "$RESPONSE" | jq -r '.content[] | select(.type == "text") | .text'
````

  
````bash
#!/usr/bin/env bash
# Ring 4: Error handling.
# Uses jq for cross-turn message-array state — building an agentic loop in shell
# requires JSON manipulation beyond ant's single-call --transform scope.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.
set -euo pipefail

run_tool() {
  case "$1" in
    create_calendar_event)
      local count
      count=$(jq '.attendees | length // 0' <<<"$2")
      if [ "$count" -gt 10 ]; then
        echo "ERROR: Too many attendees (max 10)"
        return 1
      fi
      jq -n --arg title "$(jq -r '.title' <<<"$2")" \
        '{event_id: "evt_123", status: "created", title: $title}' ;;
    list_calendar_events)
      echo '{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}' ;;
    *)
      echo "ERROR: Unknown tool: $1"
      return 1 ;;
  esac
}

EMAILS=$(seq 0 14 | sed 's/.*/user&@example.com/' | paste -sd, -)
MESSAGES=$(jq -n --arg msg "Schedule an all-hands with everyone: $EMAILS" \
  '[{role: "user", content: $msg}]')

call_api() {
  # ant reads the request body as YAML on stdin: no auth headers, no
  # hand-built JSON envelope. The static keys (model, tools) live in a
  # quoted heredoc; the growing messages array is appended as JSON,
  # which YAML accepts as flow syntax.
  {
    cat <<'YAML'
model: claude-opus-4-6
max_tokens: 1024
tools:
  - name: create_calendar_event
    description: Create a calendar event with attendees and optional recurrence.
    input_schema:
      type: object
      properties:
        title: {type: string}
        start: {type: string, format: date-time}
        end: {type: string, format: date-time}
        attendees:
          type: array
          items: {type: string, format: email}
        recurrence:
          type: object
          properties:
            frequency: {enum: [daily, weekly, monthly]}
            count: {type: integer, minimum: 1}
      required: [title, start, end]
  - name: list_calendar_events
    description: List all calendar events on a given date.
    input_schema:
      type: object
      properties:
        date: {type: string, format: date}
      required: [date]
YAML
    printf 'messages: %s\n' "$MESSAGES"
  } | ant messages create --format json
}

RESPONSE=$(call_api)

while [ "$(jq -r '.stop_reason' <<<"$RESPONSE")" = "tool_use" ]; do
  TOOL_RESULTS='[]'
  while read -r block; do
    NAME=$(jq -r '.name' <<<"$block")
    INPUT=$(jq -c '.input' <<<"$block")
    ID=$(jq -r '.id' <<<"$block")
    if OUTPUT=$(run_tool "$NAME" "$INPUT"); then
      TOOL_RESULTS=$(jq --arg id "$ID" --arg result "$OUTPUT" \
        '. + [{type: "tool_result", tool_use_id: $id, content: $result}]' \
        <<<"$TOOL_RESULTS")
    else
      # Signal failure so Claude can retry or ask for clarification.
      TOOL_RESULTS=$(jq --arg id "$ID" --arg result "$OUTPUT" \
        '. + [{type: "tool_result", tool_use_id: $id, content: $result, is_error: true}]' \
        <<<"$TOOL_RESULTS")
    fi
  done < <(jq -c '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")

  MESSAGES=$(jq \
    --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
    --argjson results "$TOOL_RESULTS" \
    '. + [
      {role: "assistant", content: $assistant},
      {role: "user", content: $results}
    ]' <<<"$MESSAGES")

  RESPONSE=$(call_api)
done

jq -r '.content[] | select(.type == "text") | .text' <<<"$RESPONSE"
````

  
````python
# Ring 4: Error handling.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

import json

import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "create_calendar_event",
        "description": "Create a calendar event with attendees and optional recurrence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "start": {"type": "string", "format": "date-time"},
                "end": {"type": "string", "format": "date-time"},
                "attendees": {
                    "type": "array",
                    "items": {"type": "string", "format": "email"},
                },
                "recurrence": {
                    "type": "object",
                    "properties": {
                        "frequency": {"enum": ["daily", "weekly", "monthly"]},
                        "count": {"type": "integer", "minimum": 1},
                    },
                },
            },
            "required": ["title", "start", "end"],
        },
    },
    {
        "name": "list_calendar_events",
        "description": "List all calendar events on a given date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "format": "date"},
            },
            "required": ["date"],
        },
    },
]


def run_tool(name, tool_input):
    if name == "create_calendar_event":
        if "attendees" in tool_input and len(tool_input["attendees"]) > 10:
            raise ValueError("Too many attendees (max 10)")
        return {"event_id": "evt_123", "status": "created", "title": tool_input["title"]}
    if name == "list_calendar_events":
        return {"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}
    raise ValueError(f"Unknown tool: {name}")


messages = [
    {
        "role": "user",
        "content": "Schedule an all-hands with everyone: " + ", ".join(f"user{i}@example.com" for i in range(15)),
    }
]

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

while response.stop_reason == "tool_use":
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            try:
                result = run_tool(block.name, block.input)
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)}
                )
            except Exception as exc:
                # Signal failure so Claude can retry or ask for clarification.
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(exc),
                        "is_error": True,
                    }
                )

    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

final_text = next(block for block in response.content if block.type == "text")
print(final_text.text)
````

  
````typescript
// Ring 4: Error handling.
// Source for <CodeSource> in build-a-tool-using-agent.mdx.

import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
  {
    name: "create_calendar_event",
    description:
      "Create a calendar event with attendees and optional recurrence.",
    input_schema: {
      type: "object",
      properties: {
        title: { type: "string" },
        start: { type: "string", format: "date-time" },
        end: { type: "string", format: "date-time" },
        attendees: {
          type: "array",
          items: { type: "string", format: "email" },
        },
        recurrence: {
          type: "object",
          properties: {
            frequency: { enum: ["daily", "weekly", "monthly"] },
            count: { type: "integer", minimum: 1 },
          },
        },
      },
      required: ["title", "start", "end"],
    },
  },
  {
    name: "list_calendar_events",
    description: "List all calendar events on a given date.",
    input_schema: {
      type: "object",
      properties: {
        date: { type: "string", format: "date" },
      },
      required: ["date"],
    },
  },
];

function runTool(name: string, input: Record<string, unknown>) {
  if (name === "create_calendar_event") {
    const attendees = input.attendees as string[] | undefined;
    if (attendees && attendees.length > 10) {
      throw new Error("Too many attendees (max 10)");
    }
    return { event_id: "evt_123", status: "created", title: input.title };
  }
  if (name === "list_calendar_events") {
    return {
      events: [{ title: "Existing meeting", start: "14:00", end: "15:00" }],
    };
  }
  throw new Error(`Unknown tool: ${name}`);
}

const emails = Array.from({ length: 15 }, (_, i) => `user${i}@example.com`);
const messages: Anthropic.MessageParam[] = [
  {
    role: "user",
    content: `Schedule an all-hands with everyone: ${emails.join(", ")}`,
  },
];

let response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools,
  messages,
});

while (response.stop_reason === "tool_use") {
  const toolResults: Anthropic.ToolResultBlockParam[] = [];
  for (const block of response.content) {
    if (block.type === "tool_use") {
      try {
        const result = runTool(block.name, block.input as Record<string, unknown>);
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: JSON.stringify(result),
        });
      } catch (err) {
        // Signal failure so Claude can retry or ask for clarification.
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: String(err),
          is_error: true,
        });
      }
    }
  }

  messages.push({ role: "assistant", content: response.content });
  messages.push({ role: "user", content: toolResults });

  response = await client.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 1024,
    tools,
    messages,
  });
}

for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
````

</CodeGroup>

**Apa yang diharapkan**

```text Output
I tried to schedule the all-hands but the calendar only allows 10 attendees per event. I can split this into two sessions, or you can let me know which 10 people to prioritize.
```

Bendera `is_error` adalah satu-satunya perbedaan dari hasil yang berhasil. Claude melihat bendera dan teks kesalahan, dan merespons sesuai. Lihat [Tangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk referensi penanganan kesalahan lengkap.

## Cincin 5: Abstraksi Tool Runner SDK

Cincin 2 hingga 4 menulis loop yang sama dengan tangan: panggil API, periksa `stop_reason`, jalankan alat, tambahkan hasil, ulangi. Tool Runner melakukan ini untuk Anda. Tentukan setiap alat sebagai fungsi, berikan daftar ke `tool_runner`, dan ambil pesan akhir setelah loop selesai. Pembungkus kesalahan, pemformatan hasil, dan manajemen percakapan ditangani secara internal.

Python SDK menggunakan dekorator `@beta_tool` untuk menyimpulkan skema dari petunjuk tipe dan docstring. TypeScript SDK menggunakan `betaZodTool` dengan skema Zod.

<Note>
Tool Runner tersedia di Python, TypeScript, dan Ruby SDK. Tab Shell dan CLI menampilkan catatan alih-alih kode; pertahankan loop Ring 4 untuk skrip berbasis shell.
</Note>

<CodeGroup>
  
````bash
#!/bin/bash
# Ring 5: The Tool Runner SDK abstraction.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

# The Tool Runner SDK abstraction is available in the Python, TypeScript,
# and Ruby SDKs. There is no equivalent for raw curl requests. Switch to
# the Python or TypeScript tab to see Ring 5, or keep the Ring 4 loop as
# your shell implementation.
````

  
````bash
#!/usr/bin/env bash
# Ring 5: The Tool Runner SDK abstraction.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.
set -euo pipefail

# The Tool Runner SDK abstraction is available in the Python, TypeScript,
# and Ruby SDKs. The ant CLI exposes the Messages API directly and has
# no equivalent helper. Switch to the Python or TypeScript tab to see
# Ring 5, or keep the Ring 4 loop as your CLI implementation.
````

  
````python
# Ring 5: The Tool Runner SDK abstraction.
# Source for <CodeSource> in build-a-tool-using-agent.mdx.

import json

import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()


@beta_tool
def create_calendar_event(
    title: str,
    start: str,
    end: str,
    attendees: list[str] | None = None,
    recurrence: dict | None = None,
) -> str:
    """Create a calendar event with attendees and optional recurrence.

    Args:
        title: Event title.
        start: Start time in ISO 8601 format.
        end: End time in ISO 8601 format.
        attendees: Email addresses to invite.
        recurrence: Dict with 'frequency' (daily, weekly, monthly) and 'count'.
    """
    if attendees and len(attendees) > 10:
        raise ValueError("Too many attendees (max 10)")
    return json.dumps({"event_id": "evt_123", "status": "created", "title": title})


@beta_tool
def list_calendar_events(date: str) -> str:
    """List all calendar events on a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    return json.dumps({"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]})


final_message = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[create_calendar_event, list_calendar_events],
    messages=[
        {
            "role": "user",
            "content": "Check what I have next Monday, then schedule a planning session that avoids any conflicts.",
        }
    ],
).until_done()

for block in final_message.content:
    if block.type == "text":
        print(block.text)
````

  
````typescript
// Ring 5: The Tool Runner SDK abstraction.
// Source for <CodeSource> in build-a-tool-using-agent.mdx.

import Anthropic from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const client = new Anthropic();

const createCalendarEvent = betaZodTool({
  name: "create_calendar_event",
  description:
    "Create a calendar event with attendees and optional recurrence.",
  inputSchema: z.object({
    title: z.string(),
    start: z.string().datetime(),
    end: z.string().datetime(),
    attendees: z.array(z.string().email()).optional(),
    recurrence: z
      .object({
        frequency: z.enum(["daily", "weekly", "monthly"]),
        count: z.number().int().min(1),
      })
      .optional(),
  }),
  run: async (input) => {
    if (input.attendees && input.attendees.length > 10) {
      throw new Error("Too many attendees (max 10)");
    }
    return JSON.stringify({
      event_id: "evt_123",
      status: "created",
      title: input.title,
    });
  },
});

const listCalendarEvents = betaZodTool({
  name: "list_calendar_events",
  description: "List all calendar events on a given date.",
  inputSchema: z.object({
    date: z.string().date(),
  }),
  run: async () => {
    return JSON.stringify({
      events: [{ title: "Existing meeting", start: "14:00", end: "15:00" }],
    });
  },
});

const finalMessage = await client.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [createCalendarEvent, listCalendarEvents],
  messages: [
    {
      role: "user",
      content:
        "Check what I have next Monday, then schedule a planning session that avoids any conflicts.",
    },
  ],
});

for (const block of finalMessage.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
````

</CodeGroup>

**Apa yang diharapkan**

```text Output
I checked your calendar for next Monday and found an existing meeting from 2pm to 3pm. I've scheduled the planning session for 10am to 11am to avoid the conflict.
```

Output identik dengan Cincin 3. Perbedaannya ada di kode: kira-kira setengah dari jumlah baris, tidak ada loop manual, dan skema hidup di samping implementasi.

## Apa yang Anda bangun

Anda memulai dengan satu panggilan alat yang dikodekan keras dan berakhir dengan agen berbentuk produksi yang menangani beberapa alat, panggilan paralel, dan kesalahan, kemudian menciutkan semuanya ke dalam Tool Runner. Sepanjang jalan Anda melihat setiap bagian dari protokol penggunaan alat: blok `tool_use`, blok `tool_result`, pencocokan `tool_use_id`, pemeriksaan `stop_reason`, dan sinyal `is_error`.

## Langkah berikutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/define-tools" title="Asah skema Anda">
    Spesifikasi skema dan praktik terbaik.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-runner" title="Penyelaman mendalam Tool Runner">
    Referensi abstraksi SDK lengkap.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use" title="Pemecahan masalah">
    Perbaiki kesalahan penggunaan alat umum.
  </Card>
</CardGroup>