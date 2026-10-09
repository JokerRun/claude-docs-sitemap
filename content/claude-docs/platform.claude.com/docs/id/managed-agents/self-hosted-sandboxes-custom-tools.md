---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools
fetched_at: 2026-10-09T02:29:51.005508Z
sha256: 7d3719a519ea70a3840fc52e05e86f71f6e38dea5f610404dd6d1fdca4f19b56
---

---
title: Alat kustom di sandbox self-hosted
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools
description: Layani alat kustom dari worker sandbox self-hosted, dan bungkus server MCP di dalam jaringan Anda sebagai alat kustom tanpa menjalankan tunnel.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

[Alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools) adalah alat yang dieksekusi oleh kode Anda sendiri: agen memancarkan event `agent.custom_tool_use` dan menunggu `user.custom_tool_result` yang sesuai. Worker Anda dapat menjadi kode tersebut. Karena berjalan di dalam sandbox Anda, alat tersebut menjangkau layanan internal, kredensial, dan "network egress" (lalu lintas jaringan keluar) yang Anda konfigurasikan untuk sandbox, dan tidak lebih dari itu.

Environment key mengotorisasi pengiriman hasil alat kustom, sehingga kunci API Claude Anda tetap berada di luar host worker.

<Note>
  Melayani alat kustom memerlukan worker SDK. Worker CLI `ant` tidak memiliki cara untuk mendaftarkan implementasi alat kustom. Dalam pola sandbox-per-sesi, [jalankan worker SDK di dalam sandbox](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#run-the-sdk-worker-inside-the-sandbox).
</Note>

## Melayani alat kustom

<Steps>
  <Step title="Deklarasikan alat pada agen">
    Tambahkan entri `custom` ke `tools` milik agen yang `name`-nya cocok dengan alat yang didaftarkan worker Anda. Lihat [Alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools) untuk bentuk deklarasi lengkapnya.

    ```json
    {
      "type": "custom",
      "name": "get_order_status",
      "description": "Look up an order in the internal fulfillment system by order ID.",
      "input_schema": {
        "type": "object",
        "properties": {
          "order_id": { "type": "string", "description": "The order ID" }
        },
        "required": ["order_id"]
      }
    }
    ```
  </Step>

  <Step title="Daftarkan implementasi dengan worker">
    Teruskan alat melalui factory `tools` (go: `ToolsFunc`) milik worker (lihat [`EnvironmentWorker`](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#environment-worker)), bersama dengan toolset bawaan:

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      import os
      from anthropic import AsyncAnthropic, beta_async_tool
      from anthropic.lib.environments import EnvironmentWorker
      from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401


      @beta_async_tool
      async def get_order_status(order_id: str) -> str:
          """Look up an order in the internal fulfillment system by order ID."""
          # Berjalan di host worker: dapat memanggil apa pun yang bisa dijangkau sandbox.
          return f"Order {order_id}: shipped"


      async def main() -> None:
          environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
          environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
          async with AsyncAnthropic(auth_token=environment_key) as client:
              await EnvironmentWorker(
                  client,
                  environment_id=environment_id,
                  environment_key=environment_key,
                  workdir="/workspace",
                  tools=lambda env: [*beta_agent_toolset_20260401(env), get_order_status],
              ).run()


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";
      import { betaTool } from "@anthropic-ai/sdk/helpers/beta/json-schema";
      import { betaAgentToolset20260401 } from "@anthropic-ai/sdk/tools/agent-toolset/node";

      const getOrderStatus = betaTool({
        name: "get_order_status",
        description: "Look up an order in the internal fulfillment system by order ID.",
        inputSchema: {
          type: "object",
          properties: { order_id: { type: "string", description: "The order ID" } },
          required: ["order_id"]
        },
        // Berjalan di host worker: panggil apa pun yang dapat dijangkau sandbox.
        run: async ({ order_id }) => `Order ${order_id}: shipped`
      });

      const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
      const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
      const client = new Anthropic({ authToken: environmentKey });
      const controller = new AbortController();
      process.once("SIGTERM", () => controller.abort());

      await new EnvironmentWorker({
        client,
        environmentId,
        environmentKey,
        workdir: "/workspace",
        signal: controller.signal,
        tools: (ctx) => [...betaAgentToolset20260401(ctx), getOrderStatus]
      }).run();
      ```

      ```csharp C#
      // EnvironmentWorker saat ini belum tersedia di SDK C#.
      // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
      ```

      ```go Go
      package main

      import (
      	"context"
      	"log"
      	"os"
      	"os/signal"
      	"syscall"

      	"github.com/anthropics/anthropic-sdk-go"
      	"github.com/anthropics/anthropic-sdk-go/lib/environments"
      	"github.com/anthropics/anthropic-sdk-go/option"
      	"github.com/anthropics/anthropic-sdk-go/toolrunner"
      	"github.com/anthropics/anthropic-sdk-go/tools/agenttoolset"
      )

      type orderStatusInput struct {
      	OrderID string `json:"order_id"`
      }

      func main() {
      	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
      	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

      	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
      	defer stop()

      	getOrderStatus := toolrunner.NewBetaTool(
      		"get_order_status",
      		"Look up an order in the internal fulfillment system by order ID.",
      		anthropic.BetaToolInputSchemaParam{
      			Properties: map[string]any{
      				"order_id": map[string]any{"type": "string", "description": "The order ID"},
      			},
      			Required: []string{"order_id"},
      		},
      		// Berjalan di host worker: dapat memanggil apa pun yang bisa dijangkau sandbox.
      		func(ctx context.Context, input orderStatusInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
      			return anthropic.BetaToolResultBlockParamContentUnion{
      				OfText: &anthropic.BetaTextBlockParam{Text: "Order " + input.OrderID + ": shipped"},
      			}, nil
      		},
      	)

      	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

      	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
      		EnvironmentID:  environmentID,
      		EnvironmentKey: environmentKey,
      		Workdir:        "/workspace",
      		ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
      			return append(agenttoolset.BetaAgentToolset20260401(env), getOrderStatus)
      		},
      	})
      	if err := worker.Run(ctx); err != nil {
      		log.Fatalf("worker: %v", err)
      	}
      }

      ```

      ```java Java
      // EnvironmentWorker saat ini belum tersedia di Java SDK.
      // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
      ```

      ```php PHP
      // EnvironmentWorker saat ini belum tersedia di PHP SDK.
      // Untuk menjawab panggilan alat kustom secara langsung, lihat stream event sesi.
      ```

      ```ruby Ruby
      # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
      # Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
      ```
    </CodeGroup>
  </Step>
</Steps>

Worker hanya menjawab alat yang didaftarkan padanya. Jika sebuah alat dideklarasikan pada agen tetapi tidak ada worker atau klien yang melayaninya, sesi akan dijeda dengan alasan berhenti `requires_action`. Sesi tetap dijeda hingga ada sesuatu yang mengirimkan hasilnya. Lihat [Menjawab panggilan alat yang menjeda sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#answer-tool-calls-that-pause-the-session) untuk alur event-nya.

## Membungkus server MCP sebagai alat kustom

[Konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) terhubung ke server MCP dari sisi Anthropic. Oleh karena itu, server harus mengekspos endpoint HTTP yang dapat dijangkau Anthropic, baik secara langsung maupun melalui [tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview).

Untuk menggunakan server yang hanya dapat dijangkau oleh jaringan Anda, jadikan worker sebagai klien MCP dan deklarasikan alat-alat server tersebut sebagai alat kustom. Server MCP tidak memerlukan konektivitas masuk dari luar jaringan Anda. Anthropic menerima definisi alat yang Anda deklarasikan pada agen, input setiap panggilan, dan hasil yang dikirimkan kembali oleh worker Anda.

Saat runtime, model memanggil alat yang dibungkus seperti alat kustom lainnya:

1. Agen memancarkan event `agent.custom_tool_use`.
2. Worker, di dalam sandbox Anda, meneruskan panggilan melalui sesi MCP yang terbuka ke server di jaringan Anda.
3. Worker mengirimkan respons server sebagai `user.custom_tool_result`.

### Menginstal SDK MCP

[Helper MCP sisi klien](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#client-side-mcp-helpers) milik SDK mengonversi alat-alat server menjadi alat yang dapat dijalankan yang diterima worker. Instal SDK MCP bersama dengan SDK Anthropic: `pip install "anthropic[mcp]" "mcp>=1.24"` (python; typescript: `npm install @modelcontextprotocol/sdk`; go: `go get github.com/modelcontextprotocol/go-sdk`).

Contoh-contoh ini terhubung tanpa autentikasi. Untuk mengirim kredensial, konfigurasikan `http_client` (typescript: `requestInit`; go: `HTTPClient`) yang Anda berikan ke transport MCP.

### Mendeklarasikan dan melayani alat

<Steps>
  <Step title="Deklarasikan alat-alat server pada agen">
    Ambil daftar alat server MCP dan deklarasikan masing-masing sebagai alat `custom`. `name`, `description`, dan `inputSchema` MCP dipetakan satu per satu ke field alat kustom. Jika server melakukan paginasi pada daftar alatnya, deklarasikan setiap halaman; worker harus mengambil daftar dari halaman yang sama.

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      from typing import Any, cast
      from anthropic import AsyncAnthropic
      from anthropic.types.beta import BetaManagedAgentsCustomToolParams
      from mcp import ClientSession, types
      # Memerlukan mcp >= 1.24, yang mengganti nama streamablehttp_client menjadi streamable_http_client.
      from mcp.client.streamable_http import streamable_http_client

      MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp"


      def to_custom_tool(tool: types.Tool) -> BetaManagedAgentsCustomToolParams:
          # Field MCP dipetakan satu-ke-satu ke deklarasi alat kustom. Cast ini
          # meneruskan dictionary skema ke parameter bertipe milik SDK tanpa perubahan.
          return {
              "type": "custom",
              "name": tool.name,
              "description": tool.description or tool.name,
              "input_schema": cast(Any, tool.inputSchema),
          }


      async def main() -> None:
          # Jalankan ini di tempat Anda membuat agen, bukan di host worker: skrip ini
          # melakukan autentikasi dengan kunci API Claude Anda (ANTHROPIC_API_KEY).
          async with (
              streamable_http_client(MCP_SERVER_URL) as (read, write, _),
              ClientSession(read, write) as mcp_session,
              AsyncAnthropic() as client,
          ):
              await mcp_session.initialize()
              listed = await mcp_session.list_tools()
              agent = await client.beta.agents.create(
                  name="Internal tools agent",
                  model="claude-opus-5-5",
                  tools=[
                      {"type": "agent_toolset_20260401"},
                      *[to_custom_tool(tool) for tool in listed.tools],
                  ],
              )
              print(agent.id)


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { Client } from "@modelcontextprotocol/sdk/client/index.js";
      import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

      const MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp";

      // Jalankan ini di tempat Anda membuat agen, bukan di host worker: kode ini
      // melakukan autentikasi dengan kunci API Claude Anda (ANTHROPIC_API_KEY).
      const client = new Anthropic();

      const mcpClient = new Client({ name: "declare-agent-tools", version: "1.0.0" });
      await mcpClient.connect(new StreamableHTTPClientTransport(new URL(MCP_SERVER_URL)));
      const { tools } = await mcpClient.listTools();

      const agent = await client.beta.agents.create({
        name: "Internal tools agent",
        model: "claude-opus-5-5",
        tools: [
          { type: "agent_toolset_20260401" },
          // Field MCP dipetakan satu-ke-satu ke deklarasi alat kustom.
          ...tools.map((tool) => ({
            type: "custom" as const,
            name: tool.name,
            description: tool.description || tool.name,
            input_schema: tool.inputSchema
          }))
        ]
      });
      console.log(agent.id);

      await mcpClient.close();
      ```

      ```csharp C#
      // Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      // C# bekerja dengan cara yang sama setelah Anda mencantumkan alat server dengan klien MCP.
      ```

      ```go Go
      package main

      import (
      	"context"
      	"encoding/json"
      	"fmt"
      	"log"

      	"github.com/anthropics/anthropic-sdk-go"
      	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
      )

      const mcpServerURL = "http://mcp.internal.example.com:8000/mcp"

      // toCustomTool memetakan satu definisi alat MCP ke deklarasi alat kustom.
      // Field-nya dipetakan satu ke satu: parameter bertipe membawa `properties` dan
      // `required`, dan setiap kata kunci JSON Schema lain yang dikeluarkan server disalurkan di
      // ExtraFields sehingga skema yang dideklarasikan cocok dengan skema server.
      func toCustomTool(tool *mcpsdk.Tool) (anthropic.BetaAgentNewParamsToolUnion, error) {
      	raw, err := json.Marshal(tool.InputSchema)
      	if err != nil {
      		return anthropic.BetaAgentNewParamsToolUnion{}, err
      	}
      	var schema map[string]any
      	if err := json.Unmarshal(raw, &schema); err != nil {
      		return anthropic.BetaAgentNewParamsToolUnion{}, err
      	}

      	inputSchema := anthropic.BetaManagedAgentsCustomToolInputSchemaParam{ExtraFields: map[string]any{}}
      	for keyword, value := range schema {
      		switch keyword {
      		case "type":
      			// Tipe parameter selalu di-marshal sebagai "type": "object".
      		case "properties":
      			properties, _ := value.(map[string]any)
      			inputSchema.Properties = properties
      		case "required":
      			entries, _ := value.([]any)
      			for _, entry := range entries {
      				if name, isString := entry.(string); isString {
      					inputSchema.Required = append(inputSchema.Required, name)
      				}
      			}
      		default:
      			inputSchema.ExtraFields[keyword] = value
      		}
      	}

      	description := tool.Description
      	if description == "" {
      		description = tool.Name
      	}
      	return anthropic.BetaAgentNewParamsToolUnion{
      		OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
      			Type:        anthropic.BetaManagedAgentsCustomToolParamsTypeCustom,
      			Name:        tool.Name,
      			Description: description,
      			InputSchema: inputSchema,
      		},
      	}, nil
      }

      func main() {
      	ctx := context.Background()

      	// Jalankan ini di mana pun Anda membuat agen, bukan di host worker: ini
      	// mengautentikasi dengan kunci API Claude Anda (ANTHROPIC_API_KEY).
      	client := anthropic.NewClient()

      	mcpClient := mcpsdk.NewClient(&mcpsdk.Implementation{Name: "declare-agent-tools", Version: "1.0.0"}, nil)
      	session, err := mcpClient.Connect(ctx, &mcpsdk.StreamableClientTransport{Endpoint: mcpServerURL}, nil)
      	if err != nil {
      		log.Fatalf("connect to MCP server: %v", err)
      	}
      	defer session.Close()

      	listed, err := session.ListTools(ctx, nil)
      	if err != nil {
      		log.Fatalf("list MCP tools: %v", err)
      	}

      	tools := []anthropic.BetaAgentNewParamsToolUnion{
      		{OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
      			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
      		}},
      	}
      	for _, tool := range listed.Tools {
      		custom, err := toCustomTool(tool)
      		if err != nil {
      			log.Fatalf("convert MCP tool %s: %v", tool.Name, err)
      		}
      		tools = append(tools, custom)
      	}

      	agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
      		Name:  "Internal tools agent",
      		Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus5_5},
      		Tools: tools,
      	})
      	if err != nil {
      		log.Fatalf("create agent: %v", err)
      	}
      	fmt.Println(agent.ID)
      }

      ```

      ```java Java
      // Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      // Java bekerja dengan cara yang sama setelah Anda mencantumkan alat server dengan klien MCP.
      ```

      ```php PHP
      // Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      // PHP bekerja dengan cara yang sama setelah Anda mencantumkan alat server dengan klien MCP.
      ```

      ```ruby Ruby
      # Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      # Ruby bekerja dengan cara yang sama setelah Anda mencantumkan alat server dengan klien MCP.
      ```
    </CodeGroup>
  </Step>

  <Step title="Layani alat dari worker">
    Hubungkan ke server MCP yang sama saat startup, konversikan alat-alatnya dengan `async_mcp_tool` (python; typescript: `mcpTools`; go: `mcp.NewBetaTools`), dan daftarkan bersama dengan `beta_agent_toolset_20260401` (python; typescript: `betaAgentToolset20260401`; go: `agenttoolset.BetaAgentToolset20260401`). Pertahankan satu sesi MCP tetap terbuka selama masa hidup worker.

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      import os
      from datetime import timedelta
      from anthropic import AsyncAnthropic
      from anthropic.lib.environments import EnvironmentWorker
      from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401
      from anthropic.lib.tools.mcp import async_mcp_tool
      from mcp import ClientSession
      # Memerlukan mcp >= 1.24, yang mengganti nama streamablehttp_client menjadi streamable_http_client.
      from mcp.client.streamable_http import streamable_http_client

      MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp"


      async def main() -> None:
          environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
          environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
          # Hubungkan ke server MCP sekali saat startup dan biarkan sesi tetap terbuka selama
          # masa hidup worker. Timeout mengubah panggilan alat yang macet menjadi hasil
          # error alih-alih panggilan yang terhenti.
          async with (
              streamable_http_client(MCP_SERVER_URL) as (read, write, _),
              ClientSession(read, write, read_timeout_seconds=timedelta(seconds=60)) as mcp_session,
              AsyncAnthropic(auth_token=environment_key) as client,
          ):
              await mcp_session.initialize()
              listed = await mcp_session.list_tools()
              mcp_tools = [async_mcp_tool(tool, mcp_session) for tool in listed.tools]
              await EnvironmentWorker(
                  client,
                  environment_id=environment_id,
                  environment_key=environment_key,
                  workdir="/workspace",
                  tools=lambda env: [*beta_agent_toolset_20260401(env), *mcp_tools],
              ).run()


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";
      import {
        mcpTools,
        type MCPCallToolResultLike,
        type MCPClientLike
      } from "@anthropic-ai/sdk/helpers/beta/mcp";
      import { betaAgentToolset20260401 } from "@anthropic-ai/sdk/tools/agent-toolset/node";
      import { Client } from "@modelcontextprotocol/sdk/client/index.js";
      import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

      const MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp";

      const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
      const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
      const client = new Anthropic({ authToken: environmentKey });
      const controller = new AbortController();
      process.once("SIGTERM", () => controller.abort());

      // Hubungkan ke server MCP sekali saat startup dan pertahankan koneksi tetap terbuka
      // selama worker berjalan.
      const mcpClient = new Client({ name: "sandbox-worker", version: "1.0.0" });
      await mcpClient.connect(new StreamableHTTPClientTransport(new URL(MCP_SERVER_URL)));
      const { tools } = await mcpClient.listTools();

      // Tipe kembalian callTool dari MCP SDK masih menyertakan bentuk hasil lawas yang
      // tidak diterima mcpTools; persempit tipenya. Hapus ini setelah MCPClientLike diperluas.
      const mcpClientForTools: MCPClientLike = {
        callTool: (params) => mcpClient.callTool(params) as Promise<MCPCallToolResultLike>
      };

      await new EnvironmentWorker({
        client,
        environmentId,
        environmentKey,
        workdir: "/workspace",
        signal: controller.signal,
        tools: (ctx) => [...betaAgentToolset20260401(ctx), ...mcpTools(tools, mcpClientForTools)]
      }).run();
      ```

      ```csharp C#
      // EnvironmentWorker saat ini belum tersedia di SDK C#.
      ```

      ```go Go
      package main

      import (
      	"context"
      	"log"
      	"os"
      	"os/signal"
      	"syscall"

      	"github.com/anthropics/anthropic-sdk-go"
      	"github.com/anthropics/anthropic-sdk-go/lib/environments"
      	"github.com/anthropics/anthropic-sdk-go/mcp"
      	"github.com/anthropics/anthropic-sdk-go/option"
      	"github.com/anthropics/anthropic-sdk-go/tools/agenttoolset"
      	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
      )

      const mcpServerURL = "http://mcp.internal.example.com:8000/mcp"

      func main() {
      	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
      	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

      	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
      	defer stop()

      	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

      	// Hubungkan ke server MCP sekali saat startup dan biarkan sesi tetap terbuka selama
      	// worker berjalan.
      	mcpClient := mcpsdk.NewClient(&mcpsdk.Implementation{Name: "sandbox-worker", Version: "1.0.0"}, nil)
      	session, err := mcpClient.Connect(ctx, &mcpsdk.StreamableClientTransport{Endpoint: mcpServerURL}, nil)
      	if err != nil {
      		log.Fatalf("connect to MCP server: %v", err)
      	}
      	defer session.Close()

      	listed, err := session.ListTools(ctx, nil)
      	if err != nil {
      		log.Fatalf("list MCP tools: %v", err)
      	}
      	mcpTools, err := mcp.NewBetaTools(listed.Tools, session)
      	if err != nil {
      		log.Fatalf("convert MCP tools: %v", err)
      	}

      	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
      		EnvironmentID:  environmentID,
      		EnvironmentKey: environmentKey,
      		Workdir:        "/workspace",
      		ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
      			return append(agenttoolset.BetaAgentToolset20260401(env), mcpTools...)
      		},
      	})
      	if err := worker.Run(ctx); err != nil {
      		log.Fatalf("worker: %v", err)
      	}
      }

      ```

      ```java Java
      // EnvironmentWorker saat ini belum tersedia di Java SDK.
      ```

      ```php PHP
      // EnvironmentWorker saat ini belum tersedia di PHP SDK.
      ```

      ```ruby Ruby
      # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
      ```
    </CodeGroup>
  </Step>
</Steps>

## Batasan dan perilaku

### Alat dideklarasikan, bukan ditemukan saat runtime

Worker mengambil daftar alat server MCP sekali saat startup dan tidak dapat menambahkan alat ke sesi yang sedang berjalan. Ketika alat-alat server berubah:

1. Deklarasikan ulang alat-alat tersebut, pada agen atau pada sesi yang sedang idle melalui [Memperbarui konfigurasi agen](https://platform.claude.com/docs/id/managed-agents/session-operations#updating-the-agent-configuration).
2. Mulai ulang worker.

### Deklarasi harus sesuai dengan Managed Agents API

Helper MCP mempertahankan nama dan deskripsi server, dan sebagian besar skema diteruskan tanpa perubahan. Ganti nama, pangkas, atau lakukan inline jika sebuah deklarasi melanggar salah satu aturan berikut:

| Field                    | Aturan                                                                                                                                                                                                                                                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                   | Unik per agen. Huruf, angka, garis bawah, dan tanda hubung, 1–128 karakter. Tidak boleh sama dengan alat agen bawaan seperti `bash` atau `read`, atau menggunakan prefiks `mcp__` yang dicadangkan.                                                                                                                      |
| `description`            | Wajib dan tidak boleh kosong.                                                                                                                                                                                                                                                                                            |
| `input_schema`           | Menerima kata kunci JSON Schema yang umum dipancarkan server MCP, seperti `additionalProperties` dan `title`. Menolak kata kunci referensi seperti `$ref` di mana pun, serta `oneOf`, `anyOf`, dan `allOf` di tingkat atas. Nama properti menggunakan huruf, angka, garis bawah, titik, dan tanda hubung, 1–64 karakter. |
| Array `tools` milik agen | Paling banyak 128 entri. Setiap alat yang dibungkus adalah satu entri, dan toolset bawaan adalah satu entri lagi.                                                                                                                                                                                                        |

Dua kasus memerlukan pekerjaan tambahan:

* **Dua server mengekspos nama alat yang sama:** Definisikan sendiri pembungkusnya dengan nama berprefiks dan buat pembungkus tersebut memanggil nama alat asli server.
* **Generator seperti pydantic memfaktorkan skema ke dalam `$defs`:** Lakukan inline pada skema tersebut sebelum Anda mendeklarasikan alat.

### Kegagalan alat muncul sebagai hasil alat error

Ketika server MCP melaporkan error alat, worker mengirimkan hasil alat error yang dapat ditanggapi oleh model. Konten MCP yang tidak memiliki padanan hasil alat, seperti blok audio dan tautan sumber daya, juga muncul sebagai error.

Tetapkan timeout pada klien MCP untuk kegagalan yang lebih cepat dan lebih jelas, seperti yang dilakukan contoh worker Python dengan `read_timeout_seconds`. Lihat [Panggilan alat MCP yang dibungkus macet](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#a-wrapped-mcp-tool-call-hangs) untuk mengetahui apa yang terjadi tanpa timeout.

### Bungkus hanya server yang Anda operasikan atau percayai

Nama, deskripsi, dan hasil alat yang dibungkus masuk ke konteks model seperti alat lainnya. Semua itu adalah input tidak tepercaya yang dapat memengaruhi apa yang dilakukan agen dengan alat-alat lainnya, termasuk `bash` pada host worker. Deklarasikan hanya alat yang Anda maksudkan untuk digunakan oleh agen.

### Kebijakan izin tidak berlaku

[Kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies#custom-tools) mengatur toolset bawaan dan toolset MCP. Worker mengeksekusi setiap panggilan alat yang dibungkus yang dibuat oleh model, jadi tempatkan langkah persetujuan apa pun di dalam kode alat Anda sendiri.
