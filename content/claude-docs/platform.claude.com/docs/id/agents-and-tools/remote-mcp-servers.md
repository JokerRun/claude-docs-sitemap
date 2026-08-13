---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: d9e42619c9b6d55a416f2ce056d4eb2b73bea93c8200ba65b859d7b3f3267a18
---

---
title: Server MCP jarak jauh
url: https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers
description: Hubungkan Claude ke server MCP jarak jauh pihak ketiga melalui API konektor MCP. Jelajahi contoh server dan tinjau langkah-langkah untuk terhubung.
---

Beberapa perusahaan telah menerapkan server MCP jarak jauh yang dapat dihubungkan oleh pengembang menggunakan API konektor MCP Anthropic. Server-server ini memperluas kemampuan yang tersedia bagi pengembang dan pengguna akhir dengan menyediakan akses jarak jauh ke berbagai layanan dan alat melalui protokol MCP.

<Note>
  Server MCP jarak jauh yang tercantum di bawah ini adalah layanan pihak ketiga yang dirancang untuk bekerja dengan Claude API. Server-server ini tidak dimiliki, dioperasikan, atau didukung oleh Anthropic. Pengguna hanya boleh terhubung ke server MCP jarak jauh yang mereka percayai dan harus meninjau praktik keamanan dan ketentuan setiap server sebelum terhubung.
</Note>

## Terhubung ke server MCP jarak jauh

Untuk terhubung ke server MCP jarak jauh:

1. Tinjau dokumentasi untuk server spesifik yang ingin Anda gunakan.
2. Pastikan Anda memiliki kredensial autentikasi yang diperlukan.
3. Ikuti instruksi koneksi khusus server yang disediakan oleh masing-masing perusahaan.

Untuk informasi lebih lanjut tentang penggunaan server MCP jarak jauh dengan Claude API, lihat [Konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector).

<Note>
  Setelah terhubung, alat MCP jarak jauh mengikuti perilaku pemicuan yang sama seperti alat lainnya. Lihat [Kapan Claude menggunakan alat MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#when-claude-uses-mcp-tools).
</Note>

## Contoh server MCP jarak jauh

<MCPServersTable platform="mcpConnector" />

<Note>
  **Mencari lebih banyak?** [Temukan ratusan server MCP lainnya di GitHub](https://github.com/modelcontextprotocol/servers).
</Note>
