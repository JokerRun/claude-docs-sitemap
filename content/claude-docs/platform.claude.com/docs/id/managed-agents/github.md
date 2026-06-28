---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/github
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 9cda88b7b6b91c4c538db1539e8df1708059006db47edd5237e5364064bbeb58
---

# Mengakses GitHub

Hubungkan agen Anda ke repositori GitHub untuk melakukan clone, membaca, dan membuat pull request.

---

Anda dapat memasang (mount) repositori GitHub ke sandbox sesi Anda dan terhubung ke GitHub MCP untuk membuat pull request.

Repositori GitHub di-cache, sehingga sesi berikutnya yang menggunakan repositori yang sama akan dimulai lebih cepat.

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## GitHub MCP dan sumber daya sesi

Pertama, buat agen yang mendeklarasikan server GitHub MCP. Definisi agen menyimpan URL server tetapi tidak menyimpan token autentikasi:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent_id=$(curl -fsS https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<JSON | jq -r '.id'
  {
    "name": "Code Reviewer",
    "model": "claude-opus-4-8",
    "system": "You are a code review assistant with access to GitHub.",
    "mcp_servers": [
      {
        "type": "url",
        "name": "github",
        "url": "https://api.githubcopilot.com/mcp/"
      }
    ],
    "tools": [
      {"type": "agent_toolset_20260401"},
      {
        "type": "mcp_toolset",
        "mcp_server_name": "github"
      }
    ]
  }
  JSON
  )
  ```

  ```bash CLI
  AGENT_ID=$(ant beta:agents create \
    --name "Code Reviewer" \
    --model '{id: claude-opus-4-8}' \
    --system "You are a code review assistant with access to GitHub." \
    --mcp-server '{type: url, name: github, url: https://api.githubcopilot.com/mcp/}' \
    --tool '{type: agent_toolset_20260401}' \
    --tool '{type: mcp_toolset, mcp_server_name: github}' \
    --transform id --raw-output)
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Code Reviewer",
      model="claude-opus-4-8",
      system="You are a code review assistant with access to GitHub.",
      mcp_servers=[
          {
              "type": "url",
              "name": "github",
              "url": "https://api.githubcopilot.com/mcp/",
          },
      ],
      tools=[
          {"type": "agent_toolset_20260401"},
          {
              "type": "mcp_toolset",
              "mcp_server_name": "github",
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Code Reviewer",
    model: "claude-opus-4-8",
    system: "You are a code review assistant with access to GitHub.",
    mcp_servers: [
      {
        type: "url",
        name: "github",
        url: "https://api.githubcopilot.com/mcp/",
      },
    ],
    tools: [
      { type: "agent_toolset_20260401" },
      {
        type: "mcp_toolset",
        mcp_server_name: "github",
      },
    ],
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Code Reviewer",
      Model = new("claude-opus-4-8"),
      System = "You are a code review assistant with access to GitHub.",
      McpServers =
      [
          new() { Type = "url", Name = "github", Url = "https://api.githubcopilot.com/mcp/" },
      ],
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
          new BetaManagedAgentsMcpToolsetParams
          {
              Type = "mcp_toolset",
              McpServerName = "github",
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Code Reviewer",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-4-8",
  	},
  	System: anthropic.String("You are a code review assistant with access to GitHub."),
  	MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{
  		{
  			Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
  			Name: "github",
  			URL:  "https://api.githubcopilot.com/mcp/",
  		},
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{
  		{
  			OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  				Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			},
  		},
  		{
  			OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
  				Type:          anthropic.BetaManagedAgentsMCPToolsetParamsTypeMCPToolset,
  				MCPServerName: "github",
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Code Reviewer")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
      .system("You are a code review assistant with access to GitHub.")
      .addMcpServer(BetaManagedAgentsUrlMcpServerParams.builder()
          .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
          .name("github")
          .url("https://api.githubcopilot.com/mcp/")
          .build())
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
          .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
          .build())
      .addTool(BetaManagedAgentsMcpToolsetParams.builder()
          .type(BetaManagedAgentsMcpToolsetParams.Type.MCP_TOOLSET)
          .mcpServerName("github")
          .build())
      .build());
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Code Reviewer',
      model: 'claude-opus-4-8',
      system: 'You are a code review assistant with access to GitHub.',
      mcpServers: [
          [
              'type' => 'url',
              'name' => 'github',
              'url' => 'https://api.githubcopilot.com/mcp/',
          ],
      ],
      tools: [
          ['type' => 'agent_toolset_20260401'],
          [
              'type' => 'mcp_toolset',
              'mcpServerName' => 'github',
          ],
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Code Reviewer",
    model: "claude-opus-4-8",
    system_: "You are a code review assistant with access to GitHub.",
    mcp_servers: [
      {
        type: "url",
        name: "github",
        url: "https://api.githubcopilot.com/mcp/"
      }
    ],
    tools: [
      {type: "agent_toolset_20260401"},
      {
        type: "mcp_toolset",
        mcp_server_name: "github"
      }
    ]
  )
  ```
</CodeGroup>

Kemudian buat sesi yang memasang repositori GitHub:

<CodeGroup>
  ```bash curl
  session_id=$(curl -fsS https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<JSON | jq -r '.id'
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "resources": [
      {
        "type": "github_repository",
        "url": "https://github.com/org/repo",
        "mount_path": "/workspace/repo",
        "authorization_token": "ghp_your_github_token"
      }
    ]
  }
  JSON
  )
  ```

  ```bash CLI
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --transform id --raw-output <<'EOF'
  resources:
    - type: github_repository
      url: https://github.com/org/repo
      mount_path: /workspace/repo
      authorization_token: ghp_your_github_token
  EOF
  )
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      resources=[
          {
              "type": "github_repository",
              "url": "https://github.com/org/repo",
              "mount_path": "/workspace/repo",
              "authorization_token": "ghp_your_github_token",
          },
      ],
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "github_repository",
        url: "https://github.com/org/repo",
        mount_path: "/workspace/repo",
        authorization_token: "ghp_your_github_token",
      },
    ],
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Resources =
      [
          new BetaManagedAgentsGitHubRepositoryResourceParams
          {
              Type = "github_repository",
              Url = "https://github.com/org/repo",
              MountPath = "/workspace/repo",
              AuthorizationToken = "ghp_your_github_token",
          },
      ],
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
  	EnvironmentID: environment.ID,
  	Resources: []anthropic.BetaSessionNewParamsResourceUnion{
  		{
  			OfGitHubRepository: &anthropic.BetaManagedAgentsGitHubRepositoryResourceParams{
  				Type:               anthropic.BetaManagedAgentsGitHubRepositoryResourceParamsTypeGitHubRepository,
  				URL:                "https://github.com/org/repo",
  				MountPath:          anthropic.String("/workspace/repo"),
  				AuthorizationToken: "ghp_your_github_token",
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .addResource(BetaManagedAgentsGitHubRepositoryResourceParams.builder()
          .type(BetaManagedAgentsGitHubRepositoryResourceParams.Type.GITHUB_REPOSITORY)
          .url("https://github.com/org/repo")
          .mountPath("/workspace/repo")
          .authorizationToken("ghp_your_github_token")
          .build())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      resources: [
          [
              'type' => 'github_repository',
              'url' => 'https://github.com/org/repo',
              'mountPath' => '/workspace/repo',
              'authorizationToken' => 'ghp_your_github_token',
          ],
      ],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "github_repository",
        url: "https://github.com/org/repo",
        mount_path: "/workspace/repo",
        authorization_token: "ghp_your_github_token"
      }
    ]
  )
  ```
</CodeGroup>

`resources[].authorization_token` mengautentikasi operasi clone repositori dan tidak ditampilkan kembali dalam respons API.

## Izin token

Saat menyediakan token GitHub, gunakan izin minimum yang diperlukan:

| Tindakan                | Scope yang diperlukan              |
| ----------------------- | ---------------------------------- |
| Clone repositori privat | `repo`                             |
| Membuat PR              | `repo`                             |
| Membaca issue           | `repo` (privat) atau `public_repo` |
| Membuat issue           | `repo` (privat) atau `public_repo` |

<Warning>
  Gunakan fine-grained personal access token dengan izin minimum yang diperlukan. Hindari menggunakan token dengan akses luas ke akun GitHub Anda.
</Warning>

## Beberapa repositori

Pasang beberapa repositori dengan menambahkan entri ke array `resources`:

<CodeGroup>
  ```bash curl
  resources='[
    {
      "type": "github_repository",
      "url": "https://github.com/org/frontend",
      "mount_path": "/workspace/frontend",
      "authorization_token": "ghp_your_github_token"
    },
    {
      "type": "github_repository",
      "url": "https://github.com/org/backend",
      "mount_path": "/workspace/backend",
      "authorization_token": "ghp_your_github_token"
    }
  ]'
  ```

  ```bash CLI
  RESOURCES_BODY=$(cat <<'EOF'
  resources:
    - type: github_repository
      url: https://github.com/org/frontend
      mount_path: /workspace/frontend
      authorization_token: ghp_your_github_token
    - type: github_repository
      url: https://github.com/org/backend
      mount_path: /workspace/backend
      authorization_token: ghp_your_github_token
  EOF
  )
  ```

  ```python Python
  resources = [
      {
          "type": "github_repository",
          "url": "https://github.com/org/frontend",
          "mount_path": "/workspace/frontend",
          "authorization_token": "ghp_your_github_token",
      },
      {
          "type": "github_repository",
          "url": "https://github.com/org/backend",
          "mount_path": "/workspace/backend",
          "authorization_token": "ghp_your_github_token",
      },
  ]
  ```

  ```typescript TypeScript
  const resources = [
    {
      type: "github_repository",
      url: "https://github.com/org/frontend",
      mount_path: "/workspace/frontend",
      authorization_token: "ghp_your_github_token",
    },
    {
      type: "github_repository",
      url: "https://github.com/org/backend",
      mount_path: "/workspace/backend",
      authorization_token: "ghp_your_github_token",
    },
  ];
  ```

  ```csharp C#
  BetaManagedAgentsGitHubRepositoryResourceParams[] resources =
  [
      new()
      {
          Type = "github_repository",
          Url = "https://github.com/org/frontend",
          MountPath = "/workspace/frontend",
          AuthorizationToken = "ghp_your_github_token",
      },
      new()
      {
          Type = "github_repository",
          Url = "https://github.com/org/backend",
          MountPath = "/workspace/backend",
          AuthorizationToken = "ghp_your_github_token",
      },
  ];
  ```

  ```go Go
  resources := []anthropic.BetaSessionNewParamsResourceUnion{
  	{
  		OfGitHubRepository: &anthropic.BetaManagedAgentsGitHubRepositoryResourceParams{
  			Type:               anthropic.BetaManagedAgentsGitHubRepositoryResourceParamsTypeGitHubRepository,
  			URL:                "https://github.com/org/frontend",
  			MountPath:          anthropic.String("/workspace/frontend"),
  			AuthorizationToken: "ghp_your_github_token",
  		},
  	},
  	{
  		OfGitHubRepository: &anthropic.BetaManagedAgentsGitHubRepositoryResourceParams{
  			Type:               anthropic.BetaManagedAgentsGitHubRepositoryResourceParamsTypeGitHubRepository,
  			URL:                "https://github.com/org/backend",
  			MountPath:          anthropic.String("/workspace/backend"),
  			AuthorizationToken: "ghp_your_github_token",
  		},
  	},
  }
  ```

  ```java Java
  var resources = List.of(
      BetaManagedAgentsGitHubRepositoryResourceParams.builder()
          .type(BetaManagedAgentsGitHubRepositoryResourceParams.Type.GITHUB_REPOSITORY)
          .url("https://github.com/org/frontend")
          .mountPath("/workspace/frontend")
          .authorizationToken("ghp_your_github_token")
          .build(),
      BetaManagedAgentsGitHubRepositoryResourceParams.builder()
          .type(BetaManagedAgentsGitHubRepositoryResourceParams.Type.GITHUB_REPOSITORY)
          .url("https://github.com/org/backend")
          .mountPath("/workspace/backend")
          .authorizationToken("ghp_your_github_token")
          .build());
  ```

  ```php PHP
  $resources = [
      [
          'type' => 'github_repository',
          'url' => 'https://github.com/org/frontend',
          'mountPath' => '/workspace/frontend',
          'authorizationToken' => 'ghp_your_github_token',
      ],
      [
          'type' => 'github_repository',
          'url' => 'https://github.com/org/backend',
          'mountPath' => '/workspace/backend',
          'authorizationToken' => 'ghp_your_github_token',
      ],
  ];
  ```

  ```ruby Ruby
  resources = [
    {
      type: "github_repository",
      url: "https://github.com/org/frontend",
      mount_path: "/workspace/frontend",
      authorization_token: "ghp_your_github_token"
    },
    {
      type: "github_repository",
      url: "https://github.com/org/backend",
      mount_path: "/workspace/backend",
      authorization_token: "ghp_your_github_token"
    }
  ]
  ```
</CodeGroup>

## Mengelola repositori pada sesi yang sedang berjalan

Setelah sesi dibuat, Anda dapat menampilkan daftar sumber daya repositorinya dan merotasi token otorisasinya. Setiap sumber daya memiliki `id` yang dikembalikan pada saat pembuatan sesi (atau melalui `resources.list`) yang Anda gunakan untuk pembaruan. Repositori terpasang selama masa hidup sesi; untuk mengubah repositori mana yang dipasang, buat sesi baru.

<CodeGroup>
  ```bash curl
  # Daftar resource pada sesi
  repo_resource_id=$(curl -fsS "https://api.anthropic.com/v1/sessions/$session_id/resources" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" | jq -r '.data[0].id')
  echo "$repo_resource_id"  # "sesrsc_01ABC..."

  # Rotasi token otorisasi
  curl -fsS "https://api.anthropic.com/v1/sessions/$session_id/resources/$repo_resource_id" \
  # ...
    -o /dev/null \
    --data @- <<JSON
  {
    "authorization_token": "ghp_your_new_github_token"
  }
  JSON
  ```

  ```bash CLI
  # Daftar resource pada session
  ant beta:sessions:resources list --session-id "$SESSION_ID"

  # Rotasi token otorisasi pada resource tertentu
  ant beta:sessions:resources update \
    --session-id "$SESSION_ID" \
    --resource-id "$RESOURCE_ID" \
    --authorization-token "ghp_your_new_github_token"
  ```

  ```python Python
  # Daftar resource pada sesi
  listed = client.beta.sessions.resources.list(session.id)
  repo_resource_id = listed.data[0].id
  print(repo_resource_id)  # "sesrsc_01ABC..."

  # Rotasi token otorisasi
  client.beta.sessions.resources.update(
      repo_resource_id,
      session_id=session.id,
      authorization_token="ghp_your_new_github_token",
  )
  ```

  ```typescript TypeScript
  // Daftar resource pada session
  const listed = await client.beta.sessions.resources.list(session.id);
  const repoResourceId = listed.data[0].id;
  console.log(repoResourceId); // "sesrsc_01ABC..."

  // Rotasi token otorisasi
  await client.beta.sessions.resources.update(repoResourceId, {
    session_id: session.id,
    authorization_token: "ghp_your_new_github_token",
  });
  ```

  ```csharp C#
  // Daftar resource pada sesi
  var listed = await client.Beta.Sessions.Resources.List(session.ID);
  var repoResourceId = (await listed.Paginate().FirstAsync()).ID;
  Console.WriteLine(repoResourceId); // "sesrsc_01ABC..."

  // Rotasi token otorisasi
  await client.Beta.Sessions.Resources.Update(repoResourceId, new()
  {
      SessionID = session.ID,
      AuthorizationToken = "ghp_your_new_github_token",
  });
  ```

  ```go Go
  // Daftar resource pada sesi
  listed, err := client.Beta.Sessions.Resources.List(ctx, session.ID, anthropic.BetaSessionResourceListParams{})
  if err != nil {
  	panic(err)
  }
  repoResourceID := listed.Data[0].ID
  fmt.Println(repoResourceID) // "sesrsc_01ABC..."

  // Rotasi token otorisasi
  _, err = client.Beta.Sessions.Resources.Update(ctx, repoResourceID, anthropic.BetaSessionResourceUpdateParams{
  	SessionID:          session.ID,
  	AuthorizationToken: "ghp_your_new_github_token",
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  // Daftar resource pada sesi
  var listed = client.beta().sessions().resources().list(session.id());
  var repoResourceId = listed.data().getFirst().asGitHubRepository().id();
  IO.println(repoResourceId);  // "sesrsc_01ABC..."

  // Rotasi token otorisasi
  client.beta().sessions().resources().update(repoResourceId, ResourceUpdateParams.builder()
      .sessionId(session.id())
      .authorizationToken("ghp_your_new_github_token")
      .build());
  ```

  ```php PHP
  // Daftar resource pada sesi
  $listed = $client->beta->sessions->resources->list($session->id);
  $repoResourceId = $listed->data[0]->id;
  echo $repoResourceId, PHP_EOL; // "sesrsc_01ABC..."

  // Rotasi token otorisasi
  $client->beta->sessions->resources->update(
      $repoResourceId,
      sessionID: $session->id,
      authorizationToken: 'ghp_your_new_github_token',
  );
  ```

  ```ruby Ruby
  # Daftar resource pada sesi
  listed = client.beta.sessions.resources.list(session.id)
  repo_resource_id = listed.data.first.id
  puts repo_resource_id # "sesrsc_01ABC..."

  # Rotasi token otorisasi
  client.beta.sessions.resources.update(
    repo_resource_id,
    session_id: session.id,
    authorization_token: "ghp_your_new_github_token"
  )
  ```
</CodeGroup>

## Membuat pull request

Dengan server GitHub MCP, agen dapat membuat branch, melakukan commit perubahan, dan melakukan push:

<CodeGroup>
  ```bash curl
  curl -fsS "https://api.anthropic.com/v1/sessions/$session_id/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -o /dev/null \
    --data @- <<JSON
  {
    "events": [
      {
        "type": "user.message",
        "content": [
          {
            "type": "text",
            "text": "Fix the type error in src/utils.ts, commit it to a new branch, and push it."
          }
        ]
      }
    ]
  }
  JSON
  ```

  ```bash CLI
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" \
    > /dev/null <<'EOF'
  events:
    - type: user.message
      content:
        - type: text
          text: Fix the type error in src/utils.ts, commit it to a new branch, and push it.
  EOF
  ```

  ```python Python
  client.beta.sessions.events.send(
      session.id,
      events=[
          {
              "type": "user.message",
              "content": [
                  {
                      "type": "text",
                      "text": "Fix the type error in src/utils.ts, commit it to a new branch, and push it.",
                  },
              ],
          },
      ],
  )
  ```

  ```typescript TypeScript
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.message",
        content: [
          {
            type: "text",
            text: "Fix the type error in src/utils.ts, commit it to a new branch, and push it.",
          },
        ],
      },
    ],
  });
  ```

  ```csharp C#
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Type = "user.message",
              Content =
              [
                  new BetaManagedAgentsTextBlock
                  {
                      Type = "text",
                      Text = "Fix the type error in src/utils.ts, commit it to a new branch, and push it.",
                  },
              ],
          },
      ],
  });
  ```

  ```go Go
  _, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{
  		{
  			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
  				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{
  					{
  						OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  							Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  							Text: "Fix the type error in src/utils.ts, commit it to a new branch, and push it.",
  						},
  					},
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().sessions().events().send(session.id(), EventSendParams.builder()
      .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
          .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
          .addContent(BetaManagedAgentsTextBlock.builder()
              .type(BetaManagedAgentsTextBlock.Type.TEXT)
              .text("Fix the type error in src/utils.ts, commit it to a new branch, and push it.")
              .build())
          .build())
      .build());
  ```

  ```php PHP
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.message',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => 'Fix the type error in src/utils.ts, commit it to a new branch, and push it.',
                  ],
              ],
          ],
      ],
  );
  ```

  ```ruby Ruby
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: "user.message",
        content: [
          {
            type: "text",
            text: "Fix the type error in src/utils.ts, commit it to a new branch, and push it."
          }
        ]
      }
    ]
  )
  ```
</CodeGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Stream event sesi" icon="lightning" href="/docs/id/managed-agents/events-and-streaming">
    Lakukan streaming event dan arahkan agen saat membuka pull request
  </Card>

  <Card title="Konektor MCP" icon="link" href="/docs/id/managed-agents/mcp-connector">
    Hubungkan lebih banyak server MCP untuk memberikan alat tambahan kepada agen
  </Card>

  <Card title="Menambahkan file" icon="file" href="/docs/id/managed-agents/files">
    Pasang file di sandbox bersama dengan repositori Anda
  </Card>
</CardGroup>
