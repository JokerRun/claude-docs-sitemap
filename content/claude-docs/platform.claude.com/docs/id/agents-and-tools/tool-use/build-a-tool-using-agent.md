---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 7bc81c44640bf277c064778e5efb0c8bdbbd0d7aa6b22f2c073e2e3f2c0520fe
---

# Tutorial: Membangun agen yang menggunakan alat

Panduan langkah demi langkah dari satu pemanggilan alat hingga loop agentik yang siap produksi.

---

Tutorial ini membangun agen pengelola kalender dalam lima lapisan konsentris. Setiap lapisan adalah program lengkap yang dapat dijalankan dan menambahkan tepat satu konsep ke lapisan sebelumnya. Pada akhirnya, Anda akan menulis loop agentik secara manual dan kemudian menggantinya dengan abstraksi SDK Tool Runner.

Alat contoh yang digunakan adalah `create_calendar_event`. Skemanya menggunakan objek bersarang, array, dan field opsional, sehingga Anda akan melihat bagaimana Claude menangani bentuk input yang realistis, bukan sekadar satu string datar.

<Note>
  Setiap lapisan dapat dijalankan secara mandiri. Salin lapisan mana pun ke dalam file baru dan kode tersebut akan berjalan tanpa memerlukan kode dari lapisan sebelumnya.
</Note>

## Lapisan 1: Satu alat, satu giliran

Program penggunaan alat sekecil mungkin: satu alat, satu pesan pengguna, satu pemanggilan alat, satu hasil. Kode ini diberi banyak komentar sehingga Anda dapat memetakan setiap baris ke [siklus hidup penggunaan alat](/docs/id/agents-and-tools/tool-use/how-tool-use-works).

Permintaan mengirimkan array `tools` bersama dengan pesan pengguna. Ketika Claude memutuskan untuk memanggil alat, respons kembali dengan `stop_reason: "tool_use"` dan blok konten `tool_use` yang berisi nama alat, `id` unik, dan `input` terstruktur. Kode Anda mengeksekusi alat tersebut, lalu mengirimkan hasilnya kembali dalam blok `tool_result` yang `tool_use_id`-nya cocok dengan `id` dari pemanggilan tersebut.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 1: Satu alat, satu giliran.

  # Definisikan satu alat sebagai fragmen JSON. input_schema adalah objek
  # JSON Schema yang mendeskripsikan argumen yang harus Claude berikan saat
  # memanggil alat ini. Skema ini mencakup objek bersarang (recurrence),
  # array (attendees), dan field opsional, yang lebih mendekati alat di
  # dunia nyata dibandingkan argumen string datar.
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

  # Kirim permintaan pengguna bersama definisi alat. Claude memutuskan
  # apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat.
  RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n \
      --argjson tools "$TOOLS" \
      --arg msg "$USER_MSG" \
      '{
        model: "claude-opus-4-8",
        max_tokens: 1024,
        tools: $tools,
        tool_choice: {type: "auto", disable_parallel_tool_use: true},
        messages: [{role: "user", content: $msg}]
      }')")

  # Ketika Claude memanggil alat, respons memiliki stop_reason "tool_use"
  # dan array content berisi blok tool_use di samping teks apa pun.
  echo "stop_reason: $(echo "$RESPONSE" | jq -r '.stop_reason')"

  # Temukan blok tool_use. Respons mungkin berisi blok teks sebelum blok
  # tool_use, jadi filter berdasarkan tipe alih-alih mengasumsikan posisi.
  TOOL_USE=$(echo "$RESPONSE" | jq '.content[] | select(.type == "tool_use")')
  TOOL_USE_ID=$(echo "$TOOL_USE" | jq -r '.id')
  echo "Tool: $(echo "$TOOL_USE" | jq -r '.name')"
  echo "Input: $(echo "$TOOL_USE" | jq -c '.input')"

  # Eksekusi alat. Di sistem nyata, ini akan memanggil API kalender Anda.
  # Di sini hasilnya di-hardcode agar contoh ini tetap mandiri.
  RESULT='{"event_id": "evt_123", "status": "created"}'

  # Kirim hasilnya kembali. Blok tool_result masuk ke pesan user dan
  # tool_use_id-nya harus cocok dengan id dari blok tool_use di atas.
  # Respons asisten sebelumnya disertakan agar Claude punya riwayat lengkap.
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
        model: "claude-opus-4-8",
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

  # Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam
  # bahasa alami dan stop_reason menjadi "end_turn".
  echo "stop_reason: $(echo "$FOLLOWUP" | jq -r '.stop_reason')"
  echo "$FOLLOWUP" | jq -r '.content[] | select(.type == "text") | .text'
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 1: Satu alat, satu giliran.
  # Menggunakan jq untuk state array pesan lintas giliran — membangun loop agentik di shell
  # memerlukan manipulasi JSON di luar cakupan --transform satu-panggilan milik ant.
  set -euo pipefail

  USER_MSG="Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am."
  MESSAGES=$(jq -n --arg msg "$USER_MSG" '[{role: "user", content: $msg}]')

  # Definisikan satu alat. input_schema adalah objek JSON Schema yang mendeskripsikan
  # argumen yang harus diteruskan Claude saat memanggil alat ini. Skema ini
  # mencakup objek bersarang (recurrence), array (attendees), dan field
  # opsional, yang lebih mendekati alat dunia nyata daripada argumen string datar.
  call_api() {
    # ant membaca body permintaan sebagai YAML di stdin: tanpa header auth, tanpa
    # amplop JSON buatan tangan. Kunci statis (model, tools, tool_choice)
    # berada di heredoc yang dikutip; array messages yang terus bertambah ditambahkan sebagai
    # JSON, yang diterima YAML sebagai sintaks flow.
    {
      cat <<'YAML'
  model: claude-opus-4-8
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

  # Kirim permintaan pengguna bersama definisi alat. Claude memutuskan
  # apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat.
  RESPONSE=$(call_api)

  # Ketika Claude memanggil alat, respons memiliki stop_reason "tool_use"
  # dan array content berisi blok tool_use di samping teks apa pun.
  echo "stop_reason: $(jq -r '.stop_reason' <<<"$RESPONSE")"

  # Temukan blok tool_use. Respons mungkin berisi blok teks sebelum
  # blok tool_use, jadi filter berdasarkan tipe alih-alih mengasumsikan posisi.
  TOOL_USE=$(jq '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")
  TOOL_USE_ID=$(jq -r '.id' <<<"$TOOL_USE")
  echo "Tool: $(jq -r '.name' <<<"$TOOL_USE")"
  echo "Input: $(jq -c '.input' <<<"$TOOL_USE")"

  # Jalankan alat. Di sistem nyata ini akan memanggil API kalender Anda.
  # Di sini hasilnya di-hardcode agar contoh tetap mandiri.
  RESULT='{"event_id": "evt_123", "status": "created"}'

  # Kirim hasilnya kembali. Blok tool_result masuk ke pesan user dan
  # tool_use_id-nya harus cocok dengan id dari blok tool_use di atas. Respons
  # asisten sebelumnya disertakan agar Claude memiliki riwayat lengkap.
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

  # Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam bahasa
  # alami dan stop_reason menjadi "end_turn".
  echo "stop_reason: $(jq -r '.stop_reason' <<<"$FOLLOWUP")"
  jq -r '.content[] | select(.type == "text") | .text' <<<"$FOLLOWUP"
  ```

  ```python Python
  # Ring 1: Satu alat, satu giliran.

  import json

  import anthropic

  # Buat klien. Klien membaca ANTHROPIC_API_KEY dari environment.
  client = anthropic.Anthropic()

  # Definisikan satu alat. input_schema adalah objek JSON Schema yang mendeskripsikan
  # argumen yang harus diteruskan Claude saat memanggil alat ini. Skema ini
  # mencakup objek bersarang (recurrence), array (attendees), dan field
  # opsional, yang lebih mendekati alat dunia nyata daripada argumen string datar.
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

  # Kirim permintaan pengguna bersama definisi alat. Claude memutuskan
  # apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat.
  response = client.messages.create(
      model="claude-opus-4-8",
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

  # Ketika Claude memanggil alat, respons memiliki stop_reason "tool_use"
  # dan array content berisi blok tool_use di samping teks apa pun.
  print(f"stop_reason: {response.stop_reason}")

  # Temukan blok tool_use. Respons mungkin berisi blok teks sebelum blok
  # tool_use, jadi pindai array content alih-alih mengasumsikan posisinya.
  tool_use = next(block for block in response.content if block.type == "tool_use")
  print(f"Tool: {tool_use.name}")
  print(f"Input: {tool_use.input}")

  # Eksekusi alat. Di sistem nyata, ini akan memanggil API kalender Anda.
  # Di sini hasilnya di-hardcode agar contoh ini tetap mandiri.
  result = {"event_id": "evt_123", "status": "created"}

  # Kirim hasilnya kembali. Blok tool_result masuk ke pesan user dan
  # tool_use_id-nya harus cocok dengan id dari blok tool_use di atas. Respons
  # asisten sebelumnya disertakan agar Claude memiliki riwayat lengkap.
  followup = client.messages.create(
      model="claude-opus-4-8",
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

  # Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam
  # bahasa alami dan stop_reason menjadi "end_turn".
  print(f"stop_reason: {followup.stop_reason}")
  final_text = next(block for block in followup.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  // Ring 1: Satu alat, satu giliran.

  import Anthropic from "@anthropic-ai/sdk";

  // Buat klien. Klien membaca ANTHROPIC_API_KEY dari environment.
  const client = new Anthropic();

  // Definisikan satu alat. input_schema adalah objek JSON Schema yang mendeskripsikan
  // argumen yang harus diteruskan Claude saat memanggil alat ini. Skema ini
  // mencakup objek bersarang (recurrence), array (attendees), dan field
  // opsional, yang lebih mendekati alat dunia nyata daripada argumen string datar.
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

  // Kirim permintaan pengguna bersama definisi alat. Claude memutuskan
  // apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat.
  const response = await client.messages.create({
    model: "claude-opus-4-8",
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

  // Ketika Claude memanggil alat, respons memiliki stop_reason "tool_use"
  // dan array content berisi blok tool_use di samping teks apa pun.
  console.log(`stop_reason: ${response.stop_reason}`);

  // Temukan blok tool_use. Respons mungkin berisi blok teks sebelum blok
  // tool_use, jadi pindai array content alih-alih mengasumsikan posisinya.
  const toolUse = response.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === "tool_use",
  )!;
  console.log(`Tool: ${toolUse.name}`);
  console.log(`Input: ${JSON.stringify(toolUse.input)}`);

  // Eksekusi alat. Di sistem nyata, ini akan memanggil API kalender Anda.
  // Di sini hasilnya di-hardcode agar contoh ini tetap mandiri.
  const result = { event_id: "evt_123", status: "created" };

  // Kirim hasilnya kembali. Blok tool_result masuk ke pesan user dan
  // tool_use_id-nya harus cocok dengan id dari blok tool_use di atas. Respons
  // assistant sebelumnya disertakan agar Claude memiliki riwayat lengkap.
  const followup = await client.messages.create({
    model: "claude-opus-4-8",
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

  // Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam
  // bahasa alami dan stop_reason menjadi "end_turn".
  console.log(`stop_reason: ${followup.stop_reason}`);
  for (const block of followup.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  // Ring 1: Satu alat, satu giliran.

  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  // Buat klien. Klien membaca ANTHROPIC_API_KEY dari environment.
  AnthropicClient client = new();

  // Definisikan satu alat. Skema input adalah objek JSON Schema yang mendeskripsikan
  // argumen yang harus diteruskan Claude saat memanggil alat ini. Skema ini
  // mencakup objek bersarang (recurrence), array (attendees), dan field
  // opsional, yang lebih mendekati alat dunia nyata daripada argumen string datar.
  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string", format = "email" },
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      }),
  ];

  // Minta paling banyak satu pemanggilan alat per giliran agar alur satu giliran di bawah
  // tetap dapat diprediksi.
  var toolChoice = new ToolChoice(new ToolChoiceAuto { DisableParallelToolUse = true });

  const string userPrompt =
      "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am.";

  // Kirim permintaan pengguna bersama definisi alat. Claude memutuskan
  // apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat tersebut.
  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = toolChoice,
      Messages = [new() { Role = Role.User, Content = userPrompt }],
  });

  // Saat Claude memanggil alat, respons memiliki stop_reason "tool_use"
  // dan array content berisi blok tool_use di samping teks apa pun.
  Console.WriteLine($"stop_reason: {response.StopReason?.Raw()}");

  // Temukan blok tool_use. Respons mungkin berisi blok teks sebelum blok
  // tool_use, jadi pindai array content alih-alih mengasumsikan posisinya.
  ToolUseBlock? toolUse = null;
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var picked))
      {
          toolUse = picked;
          break;
      }
  }
  Console.WriteLine($"Tool: {toolUse!.Name}");
  Console.WriteLine($"Input: {JsonSerializer.Serialize(toolUse.Input)}");

  // Jalankan alat. Di sistem nyata, ini akan memanggil API kalender Anda.
  // Di sini hasilnya di-hardcode agar contoh ini tetap mandiri.
  var result = """{"event_id": "evt_123", "status": "created"}""";

  // Kirim hasilnya kembali. Blok tool_result ditempatkan dalam pesan user dan
  // tool_use_id-nya harus cocok dengan id dari blok tool_use di atas. Respons
  // assistant sebelumnya disertakan agar Claude memiliki riwayat lengkap.
  List<ContentBlockParam> toolResults =
  [
      new ContentBlockParam(new ToolResultBlockParam()
      {
          ToolUseID = toolUse.ID,
          Content = result,
      }),
  ];

  var followup = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = toolChoice,
      Messages =
      [
          new() { Role = Role.User, Content = userPrompt },
          new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
          new() { Role = Role.User, Content = new MessageParamContent(toolResults) },
      ],
  });

  // Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam bahasa
  // alami dan stop_reason menjadi "end_turn".
  Console.WriteLine($"stop_reason: {followup.StopReason?.Raw()}");
  foreach (var block in followup.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 1: Satu alat, satu giliran.

  package main

  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	// Buat klien. Klien ini membaca ANTHROPIC_API_KEY dari environment.
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	// Definisikan satu alat. Skema input adalah objek JSON Schema yang mendeskripsikan
  	// argumen yang harus diteruskan Claude saat memanggil alat ini. Skema ini
  	// mencakup objek bersarang (recurrence), array (attendees), dan field
  	// opsional, yang lebih mendekati alat dunia nyata daripada argumen string datar.
  	tools := []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "create_calendar_event",
  			Description: anthropic.String("Create a calendar event with attendees and optional recurrence."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"title": map[string]any{"type": "string"},
  					"start": map[string]any{"type": "string", "format": "date-time"},
  					"end":   map[string]any{"type": "string", "format": "date-time"},
  					"attendees": map[string]any{
  						"type":  "array",
  						"items": map[string]any{"type": "string", "format": "email"},
  					},
  					"recurrence": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"frequency": map[string]any{"enum": []string{"daily", "weekly", "monthly"}},
  							"count":     map[string]any{"type": "integer", "minimum": 1},
  						},
  					},
  				},
  				Required: []string{"title", "start", "end"},
  			},
  		}},
  	}

  	// Minta paling banyak satu pemanggilan alat per giliran agar alur satu giliran di bawah
  	// tetap dapat diprediksi.
  	toolChoice := anthropic.ToolChoiceUnionParam{
  		OfAuto: &anthropic.ToolChoiceAutoParam{DisableParallelToolUse: anthropic.Bool(true)},
  	}

  	userMessage := anthropic.NewUserMessage(anthropic.NewTextBlock(
  		"Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am.",
  	))

  	// Kirim permintaan pengguna bersama dengan definisi alat. Claude memutuskan
  	// apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat tersebut.
  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:      anthropic.ModelClaudeOpus4_8,
  		MaxTokens:  1024,
  		Tools:      tools,
  		ToolChoice: toolChoice,
  		Messages:   []anthropic.MessageParam{userMessage},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Ketika Claude memanggil alat, respons memiliki stop_reason "tool_use"
  	// dan array content berisi blok tool_use di samping teks apa pun.
  	fmt.Printf("stop_reason: %s\n", response.StopReason)

  	// Temukan blok tool_use. Respons mungkin berisi blok teks sebelum blok
  	// tool_use, jadi pindai array content alih-alih mengasumsikan posisinya.
  	var toolUse anthropic.ContentBlockUnion
  	for _, block := range response.Content {
  		if block.Type == "tool_use" {
  			toolUse = block
  			break
  		}
  	}
  	fmt.Printf("Tool: %s\n", toolUse.Name)
  	fmt.Printf("Input: %s\n", string(toolUse.Input))

  	// Jalankan alat. Dalam sistem nyata, ini akan memanggil API kalender Anda.
  	// Di sini hasilnya di-hardcode agar contoh ini tetap mandiri.
  	result := `{"event_id": "evt_123", "status": "created"}`

  	// Kirim hasilnya kembali. Blok tool_result ditempatkan dalam pesan user dan
  	// tool_use_id-nya harus cocok dengan id dari blok tool_use di atas. Respons
  	// asisten sebelumnya disertakan agar Claude memiliki riwayat lengkap.
  	var assistantContent []anthropic.ContentBlockParamUnion
  	for _, block := range response.Content {
  		assistantContent = append(assistantContent, block.ToParam())
  	}

  	followup, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:      anthropic.ModelClaudeOpus4_8,
  		MaxTokens:  1024,
  		Tools:      tools,
  		ToolChoice: toolChoice,
  		Messages: []anthropic.MessageParam{
  			userMessage,
  			anthropic.NewAssistantMessage(assistantContent...),
  			anthropic.NewUserMessage(anthropic.NewToolResultBlock(toolUse.ID, result, false)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam bahasa
  	// alami dan stop_reason menjadi "end_turn".
  	fmt.Printf("stop_reason: %s\n", followup.StopReason)
  	for _, block := range followup.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 1: Satu alat, satu giliran.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolChoiceAuto;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import java.util.List;
  import java.util.Map;

  void main() {
      // Buat klien. Klien membaca ANTHROPIC_API_KEY dari environment.
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Definisikan satu alat. Skema input adalah objek JSON Schema yang mendeskripsikan
      // argumen yang harus diteruskan Claude saat memanggil alat ini. Skema ini
      // mencakup objek bersarang (recurrence), array (attendees), dan field
      // opsional, yang lebih mendekati alat dunia nyata daripada argumen string datar.
      Tool calendarTool = Tool.builder()
          .name("create_calendar_event")
          .description("Create a calendar event with attendees and optional recurrence.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "title", Map.of("type", "string"),
                  "start", Map.of("type", "string", "format", "date-time"),
                  "end", Map.of("type", "string", "format", "date-time"),
                  "attendees", Map.of(
                      "type", "array",
                      "items", Map.of("type", "string", "format", "email")
                  ),
                  "recurrence", Map.of(
                      "type", "object",
                      "properties", Map.of(
                          "frequency", Map.of("enum", List.of("daily", "weekly", "monthly")),
                          "count", Map.of("type", "integer", "minimum", 1)
                      )
                  )
              )))
              .required(List.of("title", "start", "end"))
              .build())
          .build();

      // Minta paling banyak satu pemanggilan alat per giliran agar alur satu giliran di bawah
      // tetap dapat diprediksi.
      ToolChoiceAuto toolChoice = ToolChoiceAuto.builder()
          .disableParallelToolUse(true)
          .build();

      String userPrompt =
          "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am.";

      // Kirim permintaan pengguna bersama definisi alat. Claude memutuskan
      // apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat tersebut.
      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .toolChoice(toolChoice)
          .addUserMessage(userPrompt)
          .build());

      // Ketika Claude memanggil alat, respons memiliki stop_reason "tool_use"
      // dan array content berisi blok tool_use di samping teks apa pun.
      IO.println("stop_reason: " + response.stopReason().orElse(null));

      // Temukan blok tool_use. Respons mungkin berisi blok teks sebelum blok
      // tool_use, jadi pindai array content alih-alih mengasumsikan posisinya.
      ToolUseBlock toolUse = response.content().stream()
          .flatMap(block -> block.toolUse().stream())
          .findFirst()
          .orElseThrow();
      IO.println("Tool: " + toolUse.name());
      IO.println("Input: " + toolUse._input());

      // Jalankan alat. Dalam sistem nyata, ini akan memanggil API kalender Anda.
      // Di sini hasilnya di-hardcode agar contoh ini tetap mandiri.
      String result = "{\"event_id\": \"evt_123\", \"status\": \"created\"}";

      // Kirim hasilnya kembali. Blok tool_result ditempatkan dalam pesan user dan
      // tool_use_id-nya harus cocok dengan id dari blok tool_use di atas. Respons
      // asisten sebelumnya disertakan agar Claude memiliki riwayat lengkap.
      Message followup = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .toolChoice(toolChoice)
          .addUserMessage(userPrompt)
          .addMessage(response)
          .addUserMessageOfBlockParams(List.of(ContentBlockParam.ofToolResult(
              ToolResultBlockParam.builder()
                  .toolUseId(toolUse.id())
                  .content(result)
                  .build())))
          .build());

      // Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam bahasa
      // alami dan stop_reason menjadi "end_turn".
      IO.println("stop_reason: " + followup.stopReason().orElse(null));
      followup.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 1: Satu alat, satu giliran.

  use Anthropic\Client;
  use Anthropic\Messages\ToolChoiceAuto;

  // Buat klien. Klien ini membaca ANTHROPIC_API_KEY dari environment.
  $client = new Client();

  // Definisikan satu alat. input_schema adalah objek JSON Schema yang mendeskripsikan
  // argumen yang harus diteruskan Claude saat memanggil alat ini. Skema ini
  // mencakup objek bersarang (recurrence), array (attendees), dan field
  // opsional, yang lebih mendekati alat dunia nyata daripada argumen string datar.
  $tools = [
      [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string'],
                  'start' => ['type' => 'string', 'format' => 'date-time'],
                  'end' => ['type' => 'string', 'format' => 'date-time'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string', 'format' => 'email'],
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
  ];

  $userMessage = [
      'role' => 'user',
      'content' => 'Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am.',
  ];

  // Minta paling banyak satu pemanggilan alat per giliran agar alur satu giliran di bawah
  // tetap dapat diprediksi.
  $toolChoice = ToolChoiceAuto::with(disableParallelToolUse: true);

  // Kirim permintaan pengguna bersama definisi alat. Claude memutuskan
  // apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat tersebut.
  $response = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: $tools,
      toolChoice: $toolChoice,
      messages: [$userMessage],
  );

  // Ketika Claude memanggil alat, respons memiliki stop_reason "tool_use"
  // dan array content berisi blok tool_use di samping teks apa pun.
  printf("stop_reason: %s\n", $response->stopReason);

  // Temukan blok tool_use. Respons mungkin berisi blok teks sebelum blok
  // tool_use, jadi pindai array content alih-alih mengasumsikan posisinya.
  $toolUse = null;
  foreach ($response->content as $block) {
      if ($block->type === 'tool_use') {
          $toolUse = $block;
          break;
      }
  }
  printf("Tool: %s\n", $toolUse->name);
  printf("Input: %s\n", json_encode($toolUse->input));

  // Jalankan alat. Dalam sistem nyata, ini akan memanggil API kalender Anda.
  // Di sini hasilnya di-hardcode agar contoh ini tetap mandiri.
  $result = ['event_id' => 'evt_123', 'status' => 'created'];

  // Kirim hasilnya kembali. Blok tool_result ditempatkan dalam pesan user dan
  // tool_use_id-nya harus cocok dengan id dari blok tool_use di atas. Respons
  // assistant sebelumnya disertakan agar Claude memiliki riwayat lengkap.
  $followup = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: $tools,
      toolChoice: $toolChoice,
      messages: [
          $userMessage,
          ['role' => 'assistant', 'content' => $response->content],
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => $toolUse->id,
                      'content' => json_encode($result),
                  ],
              ],
          ],
      ],
  );

  // Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam bahasa
  // alami dan stop_reason menjadi "end_turn".
  printf("stop_reason: %s\n", $followup->stopReason);
  foreach ($followup->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 1: Satu alat, satu giliran.

  require "anthropic"

  # Buat klien. Klien ini membaca ANTHROPIC_API_KEY dari environment.
  client = Anthropic::Client.new

  # Definisikan satu alat. input_schema adalah objek JSON Schema yang mendeskripsikan
  # argumen yang harus diteruskan Claude saat memanggil alat ini. Skema ini
  # mencakup objek bersarang (recurrence), array (attendees), dan field
  # opsional, yang lebih mendekati alat dunia nyata daripada argumen string datar.
  tools = [
    {
      name: "create_calendar_event",
      description: "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: {type: "string"},
          start: {type: "string", format: "date-time"},
          end: {type: "string", format: "date-time"},
          attendees: {
            type: "array",
            items: {type: "string", format: "email"}
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: {enum: ["daily", "weekly", "monthly"]},
              count: {type: "integer", minimum: 1}
            }
          }
        },
        required: ["title", "start", "end"]
      }
    }
  ]

  user_message = {
    role: "user",
    content: "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am."
  }

  # Minta paling banyak satu pemanggilan alat per giliran agar alur satu giliran di bawah
  # tetap dapat diprediksi.
  tool_choice = {type: "auto", disable_parallel_tool_use: true}

  # Kirim permintaan pengguna bersama definisi alat. Claude memutuskan
  # apakah akan memanggil alat berdasarkan permintaan dan deskripsi alat tersebut.
  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    tool_choice: tool_choice,
    messages: [user_message]
  )

  # Ketika Claude memanggil alat, respons memiliki stop_reason "tool_use"
  # dan array content berisi blok tool_use di samping teks apa pun.
  puts "stop_reason: #{response.stop_reason}"

  # Temukan blok tool_use. Respons mungkin berisi blok teks sebelum blok
  # tool_use, jadi pindai array content alih-alih mengasumsikan posisinya.
  tool_use = response.content.find { |block| block.type == :tool_use }
  puts "Tool: #{tool_use.name}"
  puts "Input: #{tool_use.input}"

  # Eksekusi alat. Di sistem nyata, ini akan memanggil API kalender Anda.
  # Di sini hasilnya di-hardcode agar contoh ini tetap mandiri.
  result = {event_id: "evt_123", status: "created"}

  # Kirim hasilnya kembali. Blok tool_result ditempatkan dalam pesan user dan
  # tool_use_id-nya harus cocok dengan id dari blok tool_use di atas. Respons
  # assistant sebelumnya disertakan agar Claude memiliki riwayat lengkap.
  followup = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    tool_choice: tool_choice,
    messages: [
      user_message,
      {role: "assistant", content: response.content},
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: tool_use.id,
            content: JSON.generate(result)
          }
        ]
      }
    ]
  )

  # Dengan hasil alat di tangan, Claude menghasilkan jawaban akhir dalam bahasa
  # alami dan stop_reason menjadi "end_turn".
  puts "stop_reason: #{followup.stop_reason}"
  followup.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**Yang diharapkan**

```text Output wrap
stop_reason: tool_use
Tool: create_calendar_event
Input: {'title': 'Sync', 'start': '2026-03-30T10:00:00', 'end': '2026-03-30T10:30:00', 'attendees': ['alice@example.com', 'bob@example.com']}
stop_reason: end_turn
I've scheduled your 30-minute sync with Alice and Bob for next Monday at 10am.
```

`stop_reason` pertama adalah `tool_use` karena Claude sedang menunggu hasil dari kalender. Setelah Anda mengirimkan hasilnya, `stop_reason` kedua adalah `end_turn` dan kontennya berupa bahasa alami untuk pengguna.

## Lapisan 2: Loop agentik

Lapisan 1 mengasumsikan Claude akan memanggil alat tepat satu kali. Tugas nyata sering kali membutuhkan beberapa pemanggilan: Claude mungkin membuat sebuah acara, membaca konfirmasinya, lalu membuat acara lain. Solusinya adalah loop `while` yang terus menjalankan alat dan mengirimkan hasilnya kembali hingga `stop_reason` tidak lagi bernilai `"tool_use"`.

Perubahan lainnya adalah riwayat percakapan. Alih-alih membangun ulang array `messages` dari awal pada setiap permintaan, simpan daftar yang terus berjalan dan tambahkan ke dalamnya. Setiap giliran melihat konteks lengkap sebelumnya.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 2: Loop agentik.

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

  # Simpan seluruh riwayat percakapan dalam array JSON agar setiap giliran melihat konteks sebelumnya.
  MESSAGES='[{"role": "user", "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."}]'

  call_api() {
    curl -s https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d "$(jq -n --argjson tools "$TOOLS" --argjson messages "$MESSAGES" \
        '{model: "claude-opus-4-8", max_tokens: 1024, tools: $tools, tool_choice: {type: "auto", disable_parallel_tool_use: true}, messages: $messages}')"
  }

  RESPONSE=$(call_api)

  # Ulangi hingga Claude berhenti meminta alat. Setiap iterasi menjalankan alat yang
  # diminta, menambahkan hasilnya ke riwayat, dan meminta Claude untuk melanjutkan.
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
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 2: Loop agentik.
  # Menggunakan jq untuk state array pesan lintas giliran — membangun loop agentik di shell
  # memerlukan manipulasi JSON di luar cakupan --transform satu-panggilan milik ant.
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

  # Simpan seluruh riwayat percakapan dalam array JSON agar setiap giliran melihat
  # konteks sebelumnya.
  MESSAGES='[{"role": "user", "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."}]'

  call_api() {
    # ant membaca body permintaan sebagai YAML di stdin: tanpa header auth, tanpa
    # amplop JSON buatan tangan. Kunci statis (model, tools, tool_choice)
    # berada dalam heredoc yang di-quote; array messages yang terus bertambah ditambahkan sebagai
    # JSON, yang diterima YAML sebagai sintaks flow.
    {
      cat <<'YAML'
  model: claude-opus-4-8
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

  # Loop hingga Claude berhenti meminta alat. Setiap iterasi menjalankan
  # alat yang diminta, menambahkan hasilnya ke riwayat, dan meminta Claude untuk
  # melanjutkan.
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
  ```

  ```python Python
  # Ring 2: Loop agentik.

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


  # Simpan seluruh riwayat percakapan dalam list agar setiap giliran melihat konteks sebelumnya.
  messages = [
      {
          "role": "user",
          "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
      }
  ]

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "auto", "disable_parallel_tool_use": True},
      messages=messages,
  )

  # Ulangi hingga Claude berhenti meminta alat. Setiap iterasi menjalankan alat
  # yang diminta, menambahkan hasilnya ke riwayat, dan meminta Claude melanjutkan.
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
          model="claude-opus-4-8",
          max_tokens=1024,
          tools=tools,
          tool_choice={"type": "auto", "disable_parallel_tool_use": True},
          messages=messages,
      )

  final_text = next(block for block in response.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  // Ring 2: Loop agentik.

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

  // Simpan seluruh riwayat percakapan agar setiap giliran melihat konteks sebelumnya.
  const messages: Anthropic.MessageParam[] = [
    {
      role: "user",
      content:
        "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
    },
  ];

  let response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools,
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages,
  });

  // Ulangi hingga Claude berhenti meminta alat. Setiap iterasi menjalankan alat
  // yang diminta, menambahkan hasilnya ke riwayat, dan meminta Claude melanjutkan.
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
      model: "claude-opus-4-8",
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
  ```

  ```csharp C#
  // Ring 2: Loop agentik.

  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string", format = "email" },
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      }),
  ];

  // Jalankan alat yang diminta dan kembalikan hasilnya sebagai string.
  string RunTool(ToolUseBlock toolUse)
  {
      if (toolUse.Name == "create_calendar_event")
      {
          var title = toolUse.Input.TryGetValue("title", out var t) ? t.GetString() : "";
          return JsonSerializer.Serialize(new { event_id = "evt_123", status = "created", title });
      }
      return JsonSerializer.Serialize(new { error = $"Unknown tool: {toolUse.Name}" });
  }

  var toolChoice = new ToolChoice(new ToolChoiceAuto { DisableParallelToolUse = true });

  // Simpan seluruh riwayat percakapan dalam sebuah list agar setiap giliran melihat konteks sebelumnya.
  List<MessageParam> messages =
  [
      new()
      {
          Role = Role.User,
          Content = "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
      },
  ];

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = toolChoice,
      Messages = messages,
  });

  // Ulangi hingga Claude berhenti meminta alat. Setiap iterasi menjalankan alat
  // yang diminta, menambahkan hasilnya ke riwayat, dan meminta Claude melanjutkan.
  while (response.StopReason == StopReason.ToolUse)
  {
      ToolUseBlock? toolUse = null;
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var picked))
          {
              toolUse = picked;
              break;
          }
      }
      var result = RunTool(toolUse!);

      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList(),
      });
      messages.Add(new()
      {
          Role = Role.User,
          Content = new MessageParamContent(
          [
              new ContentBlockParam(new ToolResultBlockParam() { ToolUseID = toolUse!.ID, Content = result }),
          ]),
      });

      response = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Tools = tools,
          ToolChoice = toolChoice,
          Messages = messages,
      });
  }

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 2: Loop agentik.

  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func runTool(name string, input map[string]any) string {
  	if name == "create_calendar_event" {
  		title, _ := input["title"].(string)
  		return fmt.Sprintf(`{"event_id": "evt_123", "status": "created", "title": %q}`, title)
  	}
  	return fmt.Sprintf(`{"error": "Unknown tool: %s"}`, name)
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	tools := []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "create_calendar_event",
  			Description: anthropic.String("Create a calendar event with attendees and optional recurrence."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"title": map[string]any{"type": "string"},
  					"start": map[string]any{"type": "string", "format": "date-time"},
  					"end":   map[string]any{"type": "string", "format": "date-time"},
  					"attendees": map[string]any{
  						"type":  "array",
  						"items": map[string]any{"type": "string", "format": "email"},
  					},
  					"recurrence": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"frequency": map[string]any{"enum": []string{"daily", "weekly", "monthly"}},
  							"count":     map[string]any{"type": "integer", "minimum": 1},
  						},
  					},
  				},
  				Required: []string{"title", "start", "end"},
  			},
  		}},
  	}

  	toolChoice := anthropic.ToolChoiceUnionParam{
  		OfAuto: &anthropic.ToolChoiceAutoParam{DisableParallelToolUse: anthropic.Bool(true)},
  	}

  	// Simpan seluruh riwayat percakapan dalam sebuah slice agar setiap giliran melihat konteks sebelumnya.
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			"Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
  		)),
  	}

  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:      anthropic.ModelClaudeOpus4_8,
  		MaxTokens:  1024,
  		Tools:      tools,
  		ToolChoice: toolChoice,
  		Messages:   messages,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Ulangi hingga Claude berhenti meminta alat. Setiap iterasi menjalankan alat yang
  	// diminta, menambahkan hasilnya ke riwayat, dan meminta Claude untuk melanjutkan.
  	for response.StopReason == "tool_use" {
  		var toolUse anthropic.ContentBlockUnion
  		for _, block := range response.Content {
  			if block.Type == "tool_use" {
  				toolUse = block
  				break
  			}
  		}

  		var input map[string]any
  		if err := json.Unmarshal(toolUse.Input, &input); err != nil {
  			log.Fatal(err)
  		}
  		result := runTool(toolUse.Name, input)

  		var assistantContent []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			assistantContent = append(assistantContent, block.ToParam())
  		}
  		messages = append(messages, anthropic.NewAssistantMessage(assistantContent...))
  		messages = append(messages, anthropic.NewUserMessage(
  			anthropic.NewToolResultBlock(toolUse.ID, result, false),
  		))

  		response, err = client.Messages.New(ctx, anthropic.MessageNewParams{
  			Model:      anthropic.ModelClaudeOpus4_8,
  			MaxTokens:  1024,
  			Tools:      tools,
  			ToolChoice: toolChoice,
  			Messages:   messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  	}

  	for _, block := range response.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 2: Loop agentik.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolChoiceAuto;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import java.util.ArrayList;
  import java.util.List;
  import java.util.Map;

  String runTool(ToolUseBlock toolUse) {
      // Input alat mentah adalah objek JSON; baca field-nya sebagai map.
      Map<String, JsonValue> input = (Map<String, JsonValue>) toolUse._input().asObject().get();
      if (toolUse.name().equals("create_calendar_event")) {
          String title = input.containsKey("title") ? input.get("title").asStringOrThrow() : "";
          return "{\"event_id\": \"evt_123\", \"status\": \"created\", \"title\": \"" + title + "\"}";
      }
      return "{\"error\": \"Unknown tool: " + toolUse.name() + "\"}";
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool calendarTool = Tool.builder()
          .name("create_calendar_event")
          .description("Create a calendar event with attendees and optional recurrence.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "title", Map.of("type", "string"),
                  "start", Map.of("type", "string", "format", "date-time"),
                  "end", Map.of("type", "string", "format", "date-time"),
                  "attendees", Map.of(
                      "type", "array",
                      "items", Map.of("type", "string", "format", "email")
                  ),
                  "recurrence", Map.of(
                      "type", "object",
                      "properties", Map.of(
                          "frequency", Map.of("enum", List.of("daily", "weekly", "monthly")),
                          "count", Map.of("type", "integer", "minimum", 1)
                      )
                  )
              )))
              .required(List.of("title", "start", "end"))
              .build())
          .build();

      ToolChoiceAuto toolChoice = ToolChoiceAuto.builder()
          .disableParallelToolUse(true)
          .build();

      // Simpan seluruh riwayat percakapan dalam list agar setiap giliran melihat konteks sebelumnya.
      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder()
          .role(MessageParam.Role.USER)
          .content("Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.")
          .build());

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .toolChoice(toolChoice)
          .messages(messages)
          .build());

      // Loop hingga Claude berhenti meminta alat. Setiap iterasi menjalankan alat yang
      // diminta, menambahkan hasilnya ke riwayat, dan meminta Claude untuk melanjutkan.
      while (response.stopReason().isPresent()
              && response.stopReason().get().equals(StopReason.TOOL_USE)) {
          ToolUseBlock toolUse = response.content().stream()
              .flatMap(block -> block.toolUse().stream())
              .findFirst()
              .orElseThrow();
          String result = runTool(toolUse);

          messages.add(response.toParam());
          messages.add(MessageParam.builder()
              .role(MessageParam.Role.USER)
              .contentOfBlockParams(List.of(ContentBlockParam.ofToolResult(
                  ToolResultBlockParam.builder()
                      .toolUseId(toolUse.id())
                      .content(result)
                      .build())))
              .build());

          response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addTool(calendarTool)
              .toolChoice(toolChoice)
              .messages(messages)
              .build());
      }

      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 2: Loop agentik.

  use Anthropic\Client;
  use Anthropic\Messages\ToolChoiceAuto;

  $client = new Client();

  $tools = [
      [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string'],
                  'start' => ['type' => 'string', 'format' => 'date-time'],
                  'end' => ['type' => 'string', 'format' => 'date-time'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string', 'format' => 'email'],
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
  ];

  function runTool(string $name, array $input): string
  {
      if ($name === 'create_calendar_event') {
          return json_encode([
              'event_id' => 'evt_123',
              'status' => 'created',
              'title' => $input['title'],
          ]);
      }

      return json_encode(['error' => "Unknown tool: {$name}"]);
  }

  $toolChoice = ToolChoiceAuto::with(disableParallelToolUse: true);

  // Simpan seluruh riwayat percakapan dalam array agar setiap giliran melihat konteks sebelumnya.
  $messages = [
      [
          'role' => 'user',
          'content' => 'Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.',
      ],
  ];

  $response = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: $tools,
      toolChoice: $toolChoice,
      messages: $messages,
  );

  // Ulangi hingga Claude berhenti meminta alat. Setiap iterasi menjalankan alat yang
  // diminta, menambahkan hasilnya ke riwayat, dan meminta Claude untuk melanjutkan.
  while ($response->stopReason === 'tool_use') {
      $toolUse = null;
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $toolUse = $block;
              break;
          }
      }

      $result = runTool($toolUse->name, $toolUse->input);

      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $messages[] = [
          'role' => 'user',
          'content' => [
              [
                  'type' => 'tool_result',
                  'tool_use_id' => $toolUse->id,
                  'content' => $result,
              ],
          ],
      ];

      $response = $client->messages->create(
          model: 'claude-opus-4-8',
          maxTokens: 1024,
          tools: $tools,
          toolChoice: $toolChoice,
          messages: $messages,
      );
  }

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 2: Loop agentik.

  require "anthropic"

  client = Anthropic::Client.new

  tools = [
    {
      name: "create_calendar_event",
      description: "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: {type: "string"},
          start: {type: "string", format: "date-time"},
          end: {type: "string", format: "date-time"},
          attendees: {
            type: "array",
            items: {type: "string", format: "email"}
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: {enum: ["daily", "weekly", "monthly"]},
              count: {type: "integer", minimum: 1}
            }
          }
        },
        required: ["title", "start", "end"]
      }
    }
  ]

  def run_tool(name, input)
    case name
    when "create_calendar_event"
      JSON.generate({event_id: "evt_123", status: "created", title: input[:title]})
    else
      JSON.generate({error: "Unknown tool: #{name}"})
    end
  end

  tool_choice = {type: "auto", disable_parallel_tool_use: true}

  # Simpan seluruh riwayat percakapan dalam array agar setiap giliran melihat konteks sebelumnya.
  messages = [
    {
      role: "user",
      content: "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."
    }
  ]

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    tool_choice: tool_choice,
    messages: messages
  )

  # Ulangi hingga Claude berhenti meminta alat. Setiap iterasi menjalankan alat yang
  # diminta, menambahkan hasilnya ke riwayat, dan meminta Claude untuk melanjutkan.
  while response.stop_reason == :tool_use
    tool_use = response.content.find { |block| block.type == :tool_use }
    result = run_tool(tool_use.name, tool_use.input)

    messages << {role: "assistant", content: response.content}
    messages << {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: tool_use.id,
          content: result
        }
      ]
    }

    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: tools,
      tool_choice: tool_choice,
      messages: messages
    )
  end

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**Yang diharapkan**

```text Output wrap
I've set up your weekly team standup for the next 4 Mondays at 9am with Alice, Bob, and Carol invited.
```

Loop mungkin berjalan sekali atau beberapa kali tergantung pada bagaimana Claude memecah tugas tersebut. Kode Anda tidak lagi perlu mengetahuinya di awal.

## Lapisan 3: Beberapa alat, pemanggilan paralel

Agen jarang hanya memiliki satu kemampuan. Tambahkan alat kedua, `list_calendar_events`, sehingga Claude dapat memeriksa jadwal yang ada sebelum membuat sesuatu yang baru.

Ketika Claude memiliki beberapa pemanggilan alat independen yang perlu dilakukan, Claude mungkin mengembalikan beberapa blok `tool_use` dalam satu respons. Loop Anda perlu memproses semuanya dan mengirimkan semua hasil bersama-sama dalam satu pesan pengguna. Iterasi setiap blok `tool_use` dalam `response.content`, bukan hanya yang pertama.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 3: Beberapa alat, panggilan paralel.

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
        '{model: "claude-opus-4-8", max_tokens: 1024, tools: $tools, messages: $messages}')"
  }

  RESPONSE=$(call_api)

  while [ "$(echo "$RESPONSE" | jq -r '.stop_reason')" = "tool_use" ]; do
    # Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
    # dan kembalikan semua hasilnya bersama dalam satu pesan user.
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
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 3: Beberapa alat, panggilan paralel.
  # Menggunakan jq untuk state array pesan lintas giliran — membangun loop agentik di shell
  # memerlukan manipulasi JSON di luar cakupan --transform satu-panggilan milik ant.
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
    # ant membaca body permintaan sebagai YAML di stdin: tanpa header auth, tanpa
    # amplop JSON buatan tangan. Kunci statis (model, tools) berada dalam
    # heredoc yang di-quote; array messages yang terus bertambah ditambahkan sebagai JSON,
    # yang diterima YAML sebagai sintaks flow.
    {
      cat <<'YAML'
  model: claude-opus-4-8
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
    # Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
    # dan kembalikan semua hasilnya bersama dalam satu pesan user.
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
  ```

  ```python Python
  # Ring 3: Beberapa alat, panggilan paralel.

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
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=tools,
      messages=messages,
  )

  while response.stop_reason == "tool_use":
      # Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
      # dan kembalikan semua hasilnya bersama dalam satu pesan user.
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
          model="claude-opus-4-8",
          max_tokens=1024,
          tools=tools,
          messages=messages,
      )

  final_text = next(block for block in response.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  // Ring 3: Beberapa alat, panggilan paralel.

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
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools,
    messages,
  });

  while (response.stop_reason === "tool_use") {
    // Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
    // dan kembalikan semua hasilnya bersama dalam satu pesan pengguna.
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
      model: "claude-opus-4-8",
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
  ```

  ```csharp C#
  // Ring 3: Beberapa alat, panggilan paralel.

  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string", format = "email" },
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      }),
      new ToolUnion(new Tool()
      {
          Name = "list_calendar_events",
          Description = "List all calendar events on a given date.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["date"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date" }),
              },
              Required = ["date"],
          },
      }),
  ];

  string RunTool(ToolUseBlock toolUse)
  {
      if (toolUse.Name == "create_calendar_event")
      {
          var title = toolUse.Input.TryGetValue("title", out var t) ? t.GetString() : "";
          return JsonSerializer.Serialize(new { event_id = "evt_123", status = "created", title });
      }
      if (toolUse.Name == "list_calendar_events")
      {
          return """{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}""";
      }
      return JsonSerializer.Serialize(new { error = $"Unknown tool: {toolUse.Name}" });
  }

  List<MessageParam> messages =
  [
      new()
      {
          Role = Role.User,
          Content = "Check what I have next Monday, then schedule a planning session that avoids any conflicts.",
      },
  ];

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      Messages = messages,
  });

  while (response.StopReason == StopReason.ToolUse)
  {
      // Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
      // dan kembalikan semua hasilnya bersama dalam satu pesan pengguna.
      List<ContentBlockParam> toolResults = [];
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              toolResults.Add(new ContentBlockParam(new ToolResultBlockParam()
              {
                  ToolUseID = toolUse.ID,
                  Content = RunTool(toolUse),
              }));
          }
      }

      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList(),
      });
      messages.Add(new() { Role = Role.User, Content = new MessageParamContent(toolResults) });

      response = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Tools = tools,
          Messages = messages,
      });
  }

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 3: Beberapa alat, panggilan paralel.

  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func runTool(name string, input map[string]any) string {
  	if name == "create_calendar_event" {
  		title, _ := input["title"].(string)
  		return fmt.Sprintf(`{"event_id": "evt_123", "status": "created", "title": %q}`, title)
  	}
  	if name == "list_calendar_events" {
  		return `{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}`
  	}
  	return fmt.Sprintf(`{"error": "Unknown tool: %s"}`, name)
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	tools := []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "create_calendar_event",
  			Description: anthropic.String("Create a calendar event with attendees and optional recurrence."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"title": map[string]any{"type": "string"},
  					"start": map[string]any{"type": "string", "format": "date-time"},
  					"end":   map[string]any{"type": "string", "format": "date-time"},
  					"attendees": map[string]any{
  						"type":  "array",
  						"items": map[string]any{"type": "string", "format": "email"},
  					},
  					"recurrence": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"frequency": map[string]any{"enum": []string{"daily", "weekly", "monthly"}},
  							"count":     map[string]any{"type": "integer", "minimum": 1},
  						},
  					},
  				},
  				Required: []string{"title", "start", "end"},
  			},
  		}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "list_calendar_events",
  			Description: anthropic.String("List all calendar events on a given date."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"date": map[string]any{"type": "string", "format": "date"},
  				},
  				Required: []string{"date"},
  			},
  		}},
  	}

  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			"Check what I have next Monday, then schedule a planning session that avoids any conflicts.",
  		)),
  	}

  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Tools:     tools,
  		Messages:  messages,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for response.StopReason == "tool_use" {
  		// Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
  		// dan kembalikan semua hasilnya bersama dalam satu pesan pengguna.
  		var toolResults []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			if block.Type == "tool_use" {
  				var input map[string]any
  				if err := json.Unmarshal(block.Input, &input); err != nil {
  					log.Fatal(err)
  				}
  				result := runTool(block.Name, input)
  				toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, result, false))
  			}
  		}

  		var assistantContent []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			assistantContent = append(assistantContent, block.ToParam())
  		}
  		messages = append(messages, anthropic.NewAssistantMessage(assistantContent...))
  		messages = append(messages, anthropic.NewUserMessage(toolResults...))

  		response, err = client.Messages.New(ctx, anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 1024,
  			Tools:     tools,
  			Messages:  messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  	}

  	for _, block := range response.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 3: Beberapa alat, panggilan paralel.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import java.util.ArrayList;
  import java.util.List;
  import java.util.Map;

  String runTool(ToolUseBlock toolUse) {
      // Input alat mentah adalah objek JSON; baca field-nya sebagai map.
      Map<String, JsonValue> input = (Map<String, JsonValue>) toolUse._input().asObject().get();
      if (toolUse.name().equals("create_calendar_event")) {
          String title = input.containsKey("title") ? input.get("title").asStringOrThrow() : "";
          return "{\"event_id\": \"evt_123\", \"status\": \"created\", \"title\": \"" + title + "\"}";
      }
      if (toolUse.name().equals("list_calendar_events")) {
          return "{\"events\": [{\"title\": \"Existing meeting\", \"start\": \"14:00\", \"end\": \"15:00\"}]}";
      }
      return "{\"error\": \"Unknown tool: " + toolUse.name() + "\"}";
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool calendarTool = Tool.builder()
          .name("create_calendar_event")
          .description("Create a calendar event with attendees and optional recurrence.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "title", Map.of("type", "string"),
                  "start", Map.of("type", "string", "format", "date-time"),
                  "end", Map.of("type", "string", "format", "date-time"),
                  "attendees", Map.of(
                      "type", "array",
                      "items", Map.of("type", "string", "format", "email")
                  ),
                  "recurrence", Map.of(
                      "type", "object",
                      "properties", Map.of(
                          "frequency", Map.of("enum", List.of("daily", "weekly", "monthly")),
                          "count", Map.of("type", "integer", "minimum", 1)
                      )
                  )
              )))
              .required(List.of("title", "start", "end"))
              .build())
          .build();

      Tool listTool = Tool.builder()
          .name("list_calendar_events")
          .description("List all calendar events on a given date.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "date", Map.of("type", "string", "format", "date")
              )))
              .required(List.of("date"))
              .build())
          .build();

      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder()
          .role(MessageParam.Role.USER)
          .content("Check what I have next Monday, then schedule a planning session that avoids any conflicts.")
          .build());

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .addTool(listTool)
          .messages(messages)
          .build());

      while (response.stopReason().isPresent()
              && response.stopReason().get().equals(StopReason.TOOL_USE)) {
          // Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
          // dan kembalikan semua hasilnya bersama dalam satu pesan user.
          List<ContentBlockParam> toolResults = new ArrayList<>();
          for (ContentBlock block : response.content()) {
              if (block.toolUse().isPresent()) {
                  ToolUseBlock toolUse = block.toolUse().get();
                  toolResults.add(ContentBlockParam.ofToolResult(
                      ToolResultBlockParam.builder()
                          .toolUseId(toolUse.id())
                          .content(runTool(toolUse))
                          .build()));
              }
          }

          messages.add(response.toParam());
          messages.add(MessageParam.builder()
              .role(MessageParam.Role.USER)
              .contentOfBlockParams(toolResults)
              .build());

          response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addTool(calendarTool)
              .addTool(listTool)
              .messages(messages)
              .build());
      }

      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 3: Beberapa alat, panggilan paralel.

  use Anthropic\Client;

  $client = new Client();

  $tools = [
      [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string'],
                  'start' => ['type' => 'string', 'format' => 'date-time'],
                  'end' => ['type' => 'string', 'format' => 'date-time'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string', 'format' => 'email'],
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
      [
          'name' => 'list_calendar_events',
          'description' => 'List all calendar events on a given date.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'date' => ['type' => 'string', 'format' => 'date'],
              ],
              'required' => ['date'],
          ],
      ],
  ];

  function runTool(string $name, array $input): string
  {
      if ($name === 'create_calendar_event') {
          return json_encode([
              'event_id' => 'evt_123',
              'status' => 'created',
              'title' => $input['title'],
          ]);
      }
      if ($name === 'list_calendar_events') {
          return json_encode([
              'events' => [['title' => 'Existing meeting', 'start' => '14:00', 'end' => '15:00']],
          ]);
      }

      return json_encode(['error' => "Unknown tool: {$name}"]);
  }

  $messages = [
      [
          'role' => 'user',
          'content' => 'Check what I have next Monday, then schedule a planning session that avoids any conflicts.',
      ],
  ];

  $response = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: $tools,
      messages: $messages,
  );

  while ($response->stopReason === 'tool_use') {
      // Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
      // dan kembalikan semua hasilnya bersama dalam satu pesan pengguna.
      $toolResults = [];
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $toolResults[] = [
                  'type' => 'tool_result',
                  'tool_use_id' => $block->id,
                  'content' => runTool($block->name, $block->input),
              ];
          }
      }

      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $messages[] = ['role' => 'user', 'content' => $toolResults];

      $response = $client->messages->create(
          model: 'claude-opus-4-8',
          maxTokens: 1024,
          tools: $tools,
          messages: $messages,
      );
  }

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 3: Beberapa alat, panggilan paralel.

  require "anthropic"

  client = Anthropic::Client.new

  tools = [
    {
      name: "create_calendar_event",
      description: "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: {type: "string"},
          start: {type: "string", format: "date-time"},
          end: {type: "string", format: "date-time"},
          attendees: {
            type: "array",
            items: {type: "string", format: "email"}
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: {enum: ["daily", "weekly", "monthly"]},
              count: {type: "integer", minimum: 1}
            }
          }
        },
        required: ["title", "start", "end"]
      }
    },
    {
      name: "list_calendar_events",
      description: "List all calendar events on a given date.",
      input_schema: {
        type: "object",
        properties: {
          date: {type: "string", format: "date"}
        },
        required: ["date"]
      }
    }
  ]

  def run_tool(name, input)
    case name
    when "create_calendar_event"
      JSON.generate({event_id: "evt_123", status: "created", title: input[:title]})
    when "list_calendar_events"
      JSON.generate({events: [{title: "Existing meeting", start: "14:00", end: "15:00"}]})
    else
      JSON.generate({error: "Unknown tool: #{name}"})
    end
  end

  messages = [
    {
      role: "user",
      content: "Check what I have next Monday, then schedule a planning session that avoids any conflicts."
    }
  ]

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    messages: messages
  )

  while response.stop_reason == :tool_use
    # Satu respons dapat berisi beberapa blok tool_use. Proses semuanya
    # dan kembalikan semua hasilnya bersama dalam satu pesan pengguna.
    tool_results = response.content.select { |block| block.type == :tool_use }.map do |tool_use|
      {
        type: "tool_result",
        tool_use_id: tool_use.id,
        content: run_tool(tool_use.name, tool_use.input)
      }
    end

    messages << {role: "assistant", content: response.content}
    messages << {role: "user", content: tool_results}

    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: tools,
      messages: messages
    )
  end

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**Yang diharapkan**

```text Output wrap
I checked your calendar for next Monday and found an existing meeting from 2pm to 3pm. I've scheduled the planning session for 10am to 11am to avoid the conflict.
```

Untuk informasi lebih lanjut tentang eksekusi konkuren dan jaminan urutan, lihat [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use).

## Lapisan 4: Penanganan error

Alat bisa gagal. API kalender mungkin menolak acara dengan terlalu banyak peserta, atau format tanggal mungkin salah. Ketika alat memunculkan error, kirimkan pesan error kembali dengan `is_error: true` alih-alih membiarkan program crash. Claude membaca error tersebut dan dapat mencoba lagi dengan input yang diperbaiki, meminta klarifikasi dari pengguna, atau menjelaskan keterbatasannya.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 4: Penanganan error.

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
        '{model: "claude-opus-4-8", max_tokens: 1024, tools: $tools, messages: $messages}')"
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
        # Sinyalkan kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
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
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 4: Penanganan error.
  # Menggunakan jq untuk state array pesan lintas-giliran — membangun loop agentik di shell
  # memerlukan manipulasi JSON di luar cakupan --transform satu-panggilan milik ant.
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
    # ant membaca body permintaan sebagai YAML di stdin: tanpa header auth, tanpa
    # envelope JSON buatan tangan. Kunci statis (model, tools) berada dalam
    # heredoc yang di-quote; array messages yang terus bertambah ditambahkan sebagai JSON,
    # yang diterima YAML sebagai sintaks flow.
    {
      cat <<'YAML'
  model: claude-opus-4-8
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
        # Sinyalkan kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
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
  ```

  ```python Python
  # Ring 4: Penanganan error.

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
      model="claude-opus-4-8",
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
                  # Sinyalkan kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
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
          model="claude-opus-4-8",
          max_tokens=1024,
          tools=tools,
          messages=messages,
      )

  final_text = next(block for block in response.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  // Ring 4: Penanganan error.

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
    model: "claude-opus-4-8",
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
          // Sinyalkan kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
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
      model: "claude-opus-4-8",
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
  ```

  ```csharp C#
  // Ring 4: Penanganan error.

  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string", format = "email" },
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      }),
      new ToolUnion(new Tool()
      {
          Name = "list_calendar_events",
          Description = "List all calendar events on a given date.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["date"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date" }),
              },
              Required = ["date"],
          },
      }),
  ];

  string RunTool(ToolUseBlock toolUse)
  {
      if (toolUse.Name == "create_calendar_event")
      {
          if (toolUse.Input.TryGetValue("attendees", out var attendees) && attendees.GetArrayLength() > 10)
          {
              throw new InvalidOperationException("Too many attendees (max 10)");
          }
          var title = toolUse.Input.TryGetValue("title", out var t) ? t.GetString() : "";
          return JsonSerializer.Serialize(new { event_id = "evt_123", status = "created", title });
      }
      if (toolUse.Name == "list_calendar_events")
      {
          return """{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}""";
      }
      throw new InvalidOperationException($"Unknown tool: {toolUse.Name}");
  }

  // Buat permintaan yang melebihi batas peserta alat agar jalur error dijalankan.
  var emails = string.Join(", ", Enumerable.Range(0, 15).Select(i => $"user{i}@example.com"));

  List<MessageParam> messages =
  [
      new() { Role = Role.User, Content = $"Schedule an all-hands with everyone: {emails}" },
  ];

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      Messages = messages,
  });

  while (response.StopReason == StopReason.ToolUse)
  {
      List<ContentBlockParam> toolResults = [];
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              ToolResultBlockParam toolResult;
              try
              {
                  toolResult = new ToolResultBlockParam() { ToolUseID = toolUse.ID, Content = RunTool(toolUse) };
              }
              catch (Exception e)
              {
                  // Sinyalkan kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
                  toolResult = new ToolResultBlockParam()
                  {
                      ToolUseID = toolUse.ID,
                      Content = e.Message,
                      IsError = true,
                  };
              }
              toolResults.Add(new ContentBlockParam(toolResult));
          }
      }

      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList(),
      });
      messages.Add(new() { Role = Role.User, Content = new MessageParamContent(toolResults) });

      response = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Tools = tools,
          Messages = messages,
      });
  }

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 4: Penanganan error.

  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"
  	"strings"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func runTool(name string, input map[string]any) (string, error) {
  	if name == "create_calendar_event" {
  		if attendees, ok := input["attendees"].([]any); ok && len(attendees) > 10 {
  			return "", fmt.Errorf("too many attendees (max 10)")
  		}
  		title, _ := input["title"].(string)
  		return fmt.Sprintf(`{"event_id": "evt_123", "status": "created", "title": %q}`, title), nil
  	}
  	if name == "list_calendar_events" {
  		return `{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}`, nil
  	}
  	return "", fmt.Errorf("unknown tool: %s", name)
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	tools := []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "create_calendar_event",
  			Description: anthropic.String("Create a calendar event with attendees and optional recurrence."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"title": map[string]any{"type": "string"},
  					"start": map[string]any{"type": "string", "format": "date-time"},
  					"end":   map[string]any{"type": "string", "format": "date-time"},
  					"attendees": map[string]any{
  						"type":  "array",
  						"items": map[string]any{"type": "string", "format": "email"},
  					},
  					"recurrence": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"frequency": map[string]any{"enum": []string{"daily", "weekly", "monthly"}},
  							"count":     map[string]any{"type": "integer", "minimum": 1},
  						},
  					},
  				},
  				Required: []string{"title", "start", "end"},
  			},
  		}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "list_calendar_events",
  			Description: anthropic.String("List all calendar events on a given date."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"date": map[string]any{"type": "string", "format": "date"},
  				},
  				Required: []string{"date"},
  			},
  		}},
  	}

  	// Buat permintaan yang melebihi batas peserta alat agar jalur error dijalankan.
  	emails := make([]string, 15)
  	for i := range emails {
  		emails[i] = fmt.Sprintf("user%d@example.com", i)
  	}
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			"Schedule an all-hands with everyone: " + strings.Join(emails, ", "),
  		)),
  	}

  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Tools:     tools,
  		Messages:  messages,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for response.StopReason == "tool_use" {
  		var toolResults []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			if block.Type == "tool_use" {
  				var input map[string]any
  				if err := json.Unmarshal(block.Input, &input); err != nil {
  					log.Fatal(err)
  				}
  				result, toolErr := runTool(block.Name, input)
  				if toolErr != nil {
  					// Sinyalkan kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
  					toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, toolErr.Error(), true))
  				} else {
  					toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, result, false))
  				}
  			}
  		}

  		var assistantContent []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			assistantContent = append(assistantContent, block.ToParam())
  		}
  		messages = append(messages, anthropic.NewAssistantMessage(assistantContent...))
  		messages = append(messages, anthropic.NewUserMessage(toolResults...))

  		response, err = client.Messages.New(ctx, anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 1024,
  			Tools:     tools,
  			Messages:  messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  	}

  	for _, block := range response.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 4: Penanganan error.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import java.util.ArrayList;
  import java.util.List;
  import java.util.Map;
  import java.util.stream.Collectors;
  import java.util.stream.IntStream;

  String runTool(ToolUseBlock toolUse) {
      // Input alat mentah adalah objek JSON; baca field-nya sebagai map.
      Map<String, JsonValue> input = (Map<String, JsonValue>) toolUse._input().asObject().get();
      if (toolUse.name().equals("create_calendar_event")) {
          int attendeeCount = input.containsKey("attendees")
              ? ((List<?>) input.get("attendees").asArray().get()).size()
              : 0;
          if (attendeeCount > 10) {
              throw new IllegalArgumentException("Too many attendees (max 10)");
          }
          String title = input.containsKey("title") ? input.get("title").asStringOrThrow() : "";
          return "{\"event_id\": \"evt_123\", \"status\": \"created\", \"title\": \"" + title + "\"}";
      }
      if (toolUse.name().equals("list_calendar_events")) {
          return "{\"events\": [{\"title\": \"Existing meeting\", \"start\": \"14:00\", \"end\": \"15:00\"}]}";
      }
      throw new IllegalArgumentException("Unknown tool: " + toolUse.name());
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool calendarTool = Tool.builder()
          .name("create_calendar_event")
          .description("Create a calendar event with attendees and optional recurrence.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "title", Map.of("type", "string"),
                  "start", Map.of("type", "string", "format", "date-time"),
                  "end", Map.of("type", "string", "format", "date-time"),
                  "attendees", Map.of(
                      "type", "array",
                      "items", Map.of("type", "string", "format", "email")
                  ),
                  "recurrence", Map.of(
                      "type", "object",
                      "properties", Map.of(
                          "frequency", Map.of("enum", List.of("daily", "weekly", "monthly")),
                          "count", Map.of("type", "integer", "minimum", 1)
                      )
                  )
              )))
              .required(List.of("title", "start", "end"))
              .build())
          .build();

      Tool listTool = Tool.builder()
          .name("list_calendar_events")
          .description("List all calendar events on a given date.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "date", Map.of("type", "string", "format", "date")
              )))
              .required(List.of("date"))
              .build())
          .build();

      // Buat permintaan yang melebihi batas peserta alat agar jalur error dijalankan.
      String emails = IntStream.range(0, 15)
          .mapToObj(i -> "user" + i + "@example.com")
          .collect(Collectors.joining(", "));

      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder()
          .role(MessageParam.Role.USER)
          .content("Schedule an all-hands with everyone: " + emails)
          .build());

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .addTool(listTool)
          .messages(messages)
          .build());

      while (response.stopReason().isPresent()
              && response.stopReason().get().equals(StopReason.TOOL_USE)) {
          List<ContentBlockParam> toolResults = new ArrayList<>();
          for (ContentBlock block : response.content()) {
              if (block.toolUse().isPresent()) {
                  ToolUseBlock toolUse = block.toolUse().get();
                  ToolResultBlockParam.Builder resultBuilder = ToolResultBlockParam.builder()
                      .toolUseId(toolUse.id());
                  try {
                      resultBuilder.content(runTool(toolUse));
                  } catch (Exception e) {
                      // Sinyalkan kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
                      resultBuilder.content(e.getMessage()).isError(true);
                  }
                  toolResults.add(ContentBlockParam.ofToolResult(resultBuilder.build()));
              }
          }

          messages.add(response.toParam());
          messages.add(MessageParam.builder()
              .role(MessageParam.Role.USER)
              .contentOfBlockParams(toolResults)
              .build());

          response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addTool(calendarTool)
              .addTool(listTool)
              .messages(messages)
              .build());
      }

      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 4: Penanganan error.

  use Anthropic\Client;

  $client = new Client();

  $tools = [
      [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string'],
                  'start' => ['type' => 'string', 'format' => 'date-time'],
                  'end' => ['type' => 'string', 'format' => 'date-time'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string', 'format' => 'email'],
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
      [
          'name' => 'list_calendar_events',
          'description' => 'List all calendar events on a given date.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'date' => ['type' => 'string', 'format' => 'date'],
              ],
              'required' => ['date'],
          ],
      ],
  ];

  function runTool(string $name, array $input): string
  {
      if ($name === 'create_calendar_event') {
          if (count($input['attendees'] ?? []) > 10) {
              throw new InvalidArgumentException('Too many attendees (max 10)');
          }

          return json_encode([
              'event_id' => 'evt_123',
              'status' => 'created',
              'title' => $input['title'],
          ]);
      }
      if ($name === 'list_calendar_events') {
          return json_encode([
              'events' => [['title' => 'Existing meeting', 'start' => '14:00', 'end' => '15:00']],
          ]);
      }

      throw new InvalidArgumentException("Unknown tool: {$name}");
  }

  // Buat permintaan yang melebihi batas peserta alat agar jalur error dijalankan.
  $emails = array_map(fn (int $i): string => "user{$i}@example.com", range(0, 14));
  $messages = [
      [
          'role' => 'user',
          'content' => 'Schedule an all-hands with everyone: ' . implode(', ', $emails),
      ],
  ];

  $response = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: $tools,
      messages: $messages,
  );

  while ($response->stopReason === 'tool_use') {
      $toolResults = [];
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              try {
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => runTool($block->name, $block->input),
                  ];
              } catch (Exception $e) {
                  // Beri sinyal kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => $e->getMessage(),
                      'is_error' => true,
                  ];
              }
          }
      }

      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $messages[] = ['role' => 'user', 'content' => $toolResults];

      $response = $client->messages->create(
          model: 'claude-opus-4-8',
          maxTokens: 1024,
          tools: $tools,
          messages: $messages,
      );
  }

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 4: Penanganan error.

  require "anthropic"

  client = Anthropic::Client.new

  tools = [
    {
      name: "create_calendar_event",
      description: "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: {type: "string"},
          start: {type: "string", format: "date-time"},
          end: {type: "string", format: "date-time"},
          attendees: {
            type: "array",
            items: {type: "string", format: "email"}
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: {enum: ["daily", "weekly", "monthly"]},
              count: {type: "integer", minimum: 1}
            }
          }
        },
        required: ["title", "start", "end"]
      }
    },
    {
      name: "list_calendar_events",
      description: "List all calendar events on a given date.",
      input_schema: {
        type: "object",
        properties: {
          date: {type: "string", format: "date"}
        },
        required: ["date"]
      }
    }
  ]

  def run_tool(name, input)
    case name
    when "create_calendar_event"
      attendees = input[:attendees]
      raise ArgumentError, "Too many attendees (max 10)" if attendees && attendees.length > 10
      JSON.generate({event_id: "evt_123", status: "created", title: input[:title]})
    when "list_calendar_events"
      JSON.generate({events: [{title: "Existing meeting", start: "14:00", end: "15:00"}]})
    else
      raise ArgumentError, "Unknown tool: #{name}"
    end
  end

  # Buat permintaan yang melebihi batas peserta alat agar jalur error dijalankan.
  emails = (0...15).map { |i| "user#{i}@example.com" }
  messages = [
    {
      role: "user",
      content: "Schedule an all-hands with everyone: #{emails.join(", ")}"
    }
  ]

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    messages: messages
  )

  while response.stop_reason == :tool_use
    tool_results = response.content.select { |block| block.type == :tool_use }.map do |tool_use|
      begin
        {
          type: "tool_result",
          tool_use_id: tool_use.id,
          content: run_tool(tool_use.name, tool_use.input)
        }
      rescue => e
        # Sinyalkan kegagalan agar Claude dapat mencoba lagi atau meminta klarifikasi.
        {
          type: "tool_result",
          tool_use_id: tool_use.id,
          content: e.message,
          is_error: true
        }
      end
    end

    messages << {role: "assistant", content: response.content}
    messages << {role: "user", content: tool_results}

    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: tools,
      messages: messages
    )
  end

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**Yang diharapkan**

```text Output wrap
I tried to schedule the all-hands but the calendar only allows 10 attendees per event. I can split this into two sessions, or you can let me know which 10 people to prioritize.
```

Flag `is_error` adalah satu-satunya perbedaan dari hasil yang berhasil. Claude melihat flag tersebut dan teks error-nya, lalu merespons sesuai dengan itu. Lihat [Menangani pemanggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk referensi lengkap penanganan error.

## Lapisan 5: Abstraksi SDK Tool Runner

Lapisan 2 hingga 4 menulis loop yang sama secara manual: memanggil API, memeriksa `stop_reason`, menjalankan alat, menambahkan hasil, ulangi. Tool Runner melakukan ini untuk Anda. Definisikan setiap alat sebagai fungsi, berikan daftarnya ke `tool_runner`, dan ambil pesan akhir setelah loop selesai. Pembungkusan error, pemformatan hasil, dan pengelolaan percakapan ditangani secara internal.

SDK Python menggunakan dekorator `@beta_tool` untuk menyimpulkan skema dari type hint dan docstring. SDK TypeScript menggunakan `betaZodTool` dengan skema Zod. SDK lainnya mengikuti pola yang sama dengan helper masing-masing: `BetaRunnableTool` di C# dan PHP, kelas alat bertipe di Java dan Ruby, serta `toolrunner.NewBetaToolFromJSONSchema` di Go.

<Note>
  Tool Runner tersedia di ketujuh SDK: Python, TypeScript, C#, Go, Java, PHP, dan Ruby. Lihat [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner) untuk referensi lengkapnya. Tab cURL dan CLI menampilkan catatan alih-alih kode; tetap gunakan loop Lapisan 4 untuk skrip berbasis curl atau CLI.
</Note>

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 5: Abstraksi Tool Runner SDK.

  # Abstraksi Tool Runner SDK tersedia di ketujuh SDK: Python,
  # TypeScript, C#, Go, Java, PHP, dan Ruby. Tidak ada padanan untuk permintaan
  # curl mentah. Beralihlah ke tab SDK mana pun untuk melihat Ring 5, atau pertahankan
  # loop Ring 4 sebagai implementasi shell Anda.
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 5: Abstraksi Tool Runner SDK.
  set -euo pipefail

  # Abstraksi Tool Runner SDK tersedia di ketujuh SDK: Python,
  # TypeScript, C#, Go, Java, PHP, dan Ruby. CLI ant mengekspos Messages
  # API secara langsung dan tidak memiliki helper yang setara. Beralihlah ke tab SDK mana pun untuk melihat
  # Ring 5, atau pertahankan loop Ring 4 sebagai implementasi CLI Anda.
  ```

  ```python Python
  # Ring 5: Abstraksi Tool Runner SDK.

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
      model="claude-opus-4-8",
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
  ```

  ```typescript TypeScript
  // Ring 5: Abstraksi Tool Runner SDK.

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
    model: "claude-opus-4-8",
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
  ```

  ```csharp C#
  // Ring 5: Abstraksi Tool Runner SDK.

  using System;
  using System.Collections.Generic;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Helpers.Beta;
  using Anthropic.Models.Beta.Messages;
  using MessageCreateParams = Anthropic.Models.Beta.Messages.MessageCreateParams;
  using InputSchema = Anthropic.Models.Beta.Messages.InputSchema;
  using Role = Anthropic.Models.Beta.Messages.Role;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  // Definisikan setiap alat sebagai runnable tool: definisinya membawa JSON Schema
  // dan callback Run menyimpan implementasinya. Melempar exception akan mengirim
  // pesan kembali ke Claude sebagai tool result dengan is_error diset.
  var createCalendarEvent = new BetaRunnableTool
  {
      Name = "create_calendar_event",
      Definition = new BetaTool
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string", description = "Event title" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", description = "Start time in ISO 8601 format" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", description = "End time in ISO 8601 format" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string" },
                      description = "Email addresses to invite",
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      },
      Run = (toolUse, _) =>
      {
          if (toolUse.Input.TryGetValue("attendees", out var attendees) && attendees.GetArrayLength() > 10)
          {
              throw new InvalidOperationException("Too many attendees (max 10)");
          }
          var title = toolUse.Input.TryGetValue("title", out var t) ? t.GetString() : "";
          return Task.FromResult<BetaToolResultBlockParamContent>(
              JsonSerializer.Serialize(new { event_id = "evt_123", status = "created", title })
          );
      },
  };

  var listCalendarEvents = new BetaRunnableTool
  {
      Name = "list_calendar_events",
      Definition = new BetaTool
      {
          Name = "list_calendar_events",
          Description = "List all calendar events on a given date.",
          InputSchema = new InputSchema
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["date"] = JsonSerializer.SerializeToElement(new { type = "string", description = "Date in YYYY-MM-DD format" }),
              },
              Required = ["date"],
          },
      },
      Run = (toolUse, _) => Task.FromResult<BetaToolResultBlockParamContent>(
          """{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}"""
      ),
  };

  // Runner memanggil API, menjalankan alat yang diminta, dan mengirim hasilnya kembali
  // hingga Claude menghasilkan jawaban akhir.
  var runner = client.Beta.Messages.ToolRunner(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "Check what I have next Monday, then schedule a planning session that avoids any conflicts.",
              },
          ],
      },
      [createCalendarEvent, listCalendarEvents]
  );

  BetaMessage? finalMessage = null;
  await foreach (var message in runner)
  {
      finalMessage = message;
  }

  foreach (var block in finalMessage!.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 5: Abstraksi Tool Runner SDK.

  package main

  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/toolrunner"
  )

  // Struct input mendefinisikan skema setiap alat. Tool runner menghasilkan
  // JSON Schema dari field struct dan tag jsonschema-nya.
  type RecurrenceInput struct {
  	Frequency string `json:"frequency,omitempty" jsonschema:"enum=daily,enum=weekly,enum=monthly,description=How often the event repeats"`
  	Count     int    `json:"count,omitempty" jsonschema:"description=Number of occurrences"`
  }

  type CreateCalendarEventInput struct {
  	Title      string           `json:"title" jsonschema:"required,description=Event title"`
  	Start      string           `json:"start" jsonschema:"required,description=Start time in ISO 8601 format"`
  	End        string           `json:"end" jsonschema:"required,description=End time in ISO 8601 format"`
  	Attendees  []string         `json:"attendees,omitempty" jsonschema:"description=Email addresses to invite"`
  	Recurrence *RecurrenceInput `json:"recurrence,omitempty"`
  }

  type ListCalendarEventsInput struct {
  	Date string `json:"date" jsonschema:"required,description=Date in YYYY-MM-DD format"`
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	// Definisikan setiap alat sebagai fungsi handler. Mengembalikan error akan mengirim
  	// pesan kembali ke Claude sebagai tool result dengan is_error diset.
  	createCalendarEvent, err := toolrunner.NewBetaToolFromJSONSchema(
  		"create_calendar_event",
  		"Create a calendar event with attendees and optional recurrence.",
  		func(ctx context.Context, input CreateCalendarEventInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
  			if len(input.Attendees) > 10 {
  				return anthropic.BetaToolResultBlockParamContentUnion{}, fmt.Errorf("too many attendees (max 10)")
  			}
  			return anthropic.BetaToolResultBlockParamContentUnion{
  				OfText: &anthropic.BetaTextBlockParam{
  					Text: fmt.Sprintf(`{"event_id": "evt_123", "status": "created", "title": %q}`, input.Title),
  				},
  			}, nil
  		},
  	)
  	if err != nil {
  		log.Fatal(err)
  	}

  	listCalendarEvents, err := toolrunner.NewBetaToolFromJSONSchema(
  		"list_calendar_events",
  		"List all calendar events on a given date.",
  		func(ctx context.Context, input ListCalendarEventsInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
  			return anthropic.BetaToolResultBlockParamContentUnion{
  				OfText: &anthropic.BetaTextBlockParam{
  					Text: `{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}`,
  				},
  			}, nil
  		},
  	)
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Runner memanggil API, menjalankan alat yang diminta, dan mengirim hasilnya kembali
  	// hingga Claude menghasilkan jawaban akhir.
  	runner := client.Beta.Messages.NewToolRunner(
  		[]anthropic.BetaTool{createCalendarEvent, listCalendarEvents},
  		anthropic.BetaToolRunnerParams{
  			BetaMessageNewParams: anthropic.BetaMessageNewParams{
  				Model:     anthropic.ModelClaudeOpus4_8,
  				MaxTokens: 1024,
  				Messages: []anthropic.BetaMessageParam{
  					anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(
  						"Check what I have next Monday, then schedule a planning session that avoids any conflicts.",
  					)),
  				},
  			},
  		},
  	)

  	var finalMessage *anthropic.BetaMessage
  	for message, err := range runner.All(ctx) {
  		if err != nil {
  			log.Fatal(err)
  		}
  		finalMessage = message
  	}

  	for _, block := range finalMessage.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 5: Abstraksi Tool Runner SDK.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.helpers.BetaToolRunner;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.fasterxml.jackson.annotation.JsonClassDescription;
  import com.fasterxml.jackson.annotation.JsonPropertyDescription;
  import java.util.List;
  import java.util.function.Supplier;

  // Definisikan setiap alat sebagai kelas: field-nya mendeskripsikan skema input, dan
  // metode get() berisi implementasinya. Melempar exception akan mengirim
  // pesan kembali ke Claude sebagai tool result dengan is_error diset.
  @JsonClassDescription("Create a calendar event with attendees.")
  static class CreateCalendarEvent implements Supplier<String> {
      @JsonPropertyDescription("Event title")
      public String title;

      @JsonPropertyDescription("Start time in ISO 8601 format")
      public String start;

      @JsonPropertyDescription("End time in ISO 8601 format")
      public String end;

      @JsonPropertyDescription("Email addresses to invite")
      public List<String> attendees;

      @Override
      public String get() {
          if (attendees != null && attendees.size() > 10) {
              throw new IllegalArgumentException("Too many attendees (max 10)");
          }
          return "{\"event_id\": \"evt_123\", \"status\": \"created\", \"title\": \"" + title + "\"}";
      }
  }

  @JsonClassDescription("List all calendar events on a given date.")
  static class ListCalendarEvents implements Supplier<String> {
      @JsonPropertyDescription("Date in YYYY-MM-DD format")
      public String date;

      @Override
      public String get() {
          return "{\"events\": [{\"title\": \"Existing meeting\", \"start\": \"14:00\", \"end\": \"15:00\"}]}";
      }
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Runner memanggil API, menjalankan alat yang diminta, dan mengirim balik hasilnya
      // hingga Claude menghasilkan jawaban akhir.
      BetaToolRunner runner = client.beta()
              .messages()
              .toolRunner(MessageCreateParams.builder()
                      .model(Model.CLAUDE_OPUS_4_8)
                      .maxTokens(1024)
                      .addBeta("structured-outputs-2025-11-13")
                      .addUserMessage("Check what I have next Monday, then schedule a planning session that avoids any conflicts.")
                      .addTool(CreateCalendarEvent.class)
                      .addTool(ListCalendarEvents.class)
                      .build());

      BetaMessage finalMessage = null;
      for (BetaMessage message : runner) {
          finalMessage = message;
      }

      finalMessage.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 5: Abstraksi Tool Runner SDK.

  use Anthropic\Client;
  use Anthropic\Lib\Tools\BetaRunnableTool;
  use Anthropic\Messages\Model;

  $client = new Client();

  // Definisikan setiap alat sebagai alat yang dapat dijalankan: definisinya membawa JSON Schema
  // dan closure `run` menyimpan implementasinya. Melempar exception akan mengirim
  // pesan kembali ke Claude sebagai tool result dengan is_error diset.
  $createCalendarEvent = new BetaRunnableTool(
      definition: [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string', 'description' => 'Event title'],
                  'start' => ['type' => 'string', 'description' => 'Start time in ISO 8601 format'],
                  'end' => ['type' => 'string', 'description' => 'End time in ISO 8601 format'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string'],
                      'description' => 'Email addresses to invite',
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
      run: function (array $input): string {
          if (count($input['attendees'] ?? []) > 10) {
              throw new InvalidArgumentException('Too many attendees (max 10)');
          }

          return json_encode([
              'event_id' => 'evt_123',
              'status' => 'created',
              'title' => $input['title'],
          ]);
      },
  );

  $listCalendarEvents = new BetaRunnableTool(
      definition: [
          'name' => 'list_calendar_events',
          'description' => 'List all calendar events on a given date.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'date' => ['type' => 'string', 'description' => 'Date in YYYY-MM-DD format'],
              ],
              'required' => ['date'],
          ],
      ],
      run: fn (array $input): string => json_encode([
          'events' => [['title' => 'Existing meeting', 'start' => '14:00', 'end' => '15:00']],
      ]),
  );

  // Runner memanggil API, menjalankan alat yang diminta, dan mengumpankan hasilnya kembali
  // hingga Claude menghasilkan jawaban akhir.
  $runner = $client->beta->messages->toolRunner(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => 'Check what I have next Monday, then schedule a planning session that avoids any conflicts.',
          ],
      ],
      model: Model::CLAUDE_OPUS_4_8,
      tools: [$createCalendarEvent, $listCalendarEvents],
  );

  $finalMessage = null;
  foreach ($runner as $message) {
      $finalMessage = $message;
  }

  foreach ($finalMessage->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 5: Abstraksi Tool Runner SDK.

  require "anthropic"

  client = Anthropic::Client.new

  # Definisikan setiap alat sebagai kelas: model input bertipe mendeskripsikan skema, dan
  # metode call berisi implementasinya. Memunculkan error akan mengirim pesan
  # kembali ke Claude sebagai hasil alat dengan is_error diaktifkan.
  class RecurrenceInput < Anthropic::BaseModel
    optional :frequency, Anthropic::InputSchema::EnumOf["daily", "weekly", "monthly"],
             doc: "How often the event repeats"
    optional :count, Integer, doc: "Number of occurrences"
  end

  class CreateCalendarEventInput < Anthropic::BaseModel
    required :title, String, doc: "Event title"
    required :start, String, doc: "Start time in ISO 8601 format"
    required :end, String, doc: "End time in ISO 8601 format"
    optional :attendees, Anthropic::InputSchema::ArrayOf[String], doc: "Email addresses to invite"
    optional :recurrence, RecurrenceInput, doc: "Optional recurrence rule"
  end

  class CreateCalendarEvent < Anthropic::BaseTool
    doc "Create a calendar event with attendees and optional recurrence."
    input_schema CreateCalendarEventInput

    def call(input)
      raise ArgumentError, "Too many attendees (max 10)" if input.attendees && input.attendees.length > 10
      JSON.generate({event_id: "evt_123", status: "created", title: input.title})
    end
  end

  class ListCalendarEventsInput < Anthropic::BaseModel
    required :date, String, doc: "Date in YYYY-MM-DD format"
  end

  class ListCalendarEvents < Anthropic::BaseTool
    doc "List all calendar events on a given date."
    input_schema ListCalendarEventsInput

    def call(input)
      JSON.generate({events: [{title: "Existing meeting", start: "14:00", end: "15:00"}]})
    end
  end

  # Runner memanggil API, menjalankan alat yang diminta, dan mengembalikan hasilnya
  # hingga Claude menghasilkan jawaban akhir.
  runner = client.beta.messages.tool_runner(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [CreateCalendarEvent.new, ListCalendarEvents.new],
    messages: [
      {
        role: "user",
        content: "Check what I have next Monday, then schedule a planning session that avoids any conflicts."
      }
    ]
  )

  final_message = nil
  runner.each_message { |message| final_message = message }

  final_message.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**Yang diharapkan**

```text Output wrap
I checked your calendar for next Monday and found an existing meeting from 2pm to 3pm. I've scheduled the planning session for 10am to 11am to avoid the conflict.
```

Output-nya identik dengan Lapisan 3. Perbedaannya ada pada kode: kira-kira setengah jumlah baris, tanpa loop manual, dan skema berada tepat di samping implementasinya.

## Apa yang telah Anda bangun

Anda memulai dengan satu pemanggilan alat yang di-hardcode dan berakhir dengan agen berbentuk produksi yang menangani beberapa alat, pemanggilan paralel, dan error, lalu meringkas semua itu ke dalam Tool Runner. Sepanjang proses, Anda telah melihat setiap bagian dari protokol penggunaan alat: blok `tool_use`, blok `tool_result`, pencocokan `tool_use_id`, pemeriksaan `stop_reason`, dan penandaan `is_error`.

## Langkah selanjutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/define-tools" title="Mendefinisikan alat">
    Spesifikasi skema dan praktik terbaik.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/tool-runner" title="Pendalaman Tool Runner">
    Referensi lengkap abstraksi SDK.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use" title="Pemecahan masalah">
    Perbaiki error umum penggunaan alat.
  </Card>
</CardGroup>
