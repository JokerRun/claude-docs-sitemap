---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 06c95bf8bcc2ba9714c35edb2d3cdd7fe6e7330744a308bd3862fbacaeb0736d
---

---
title: Server MCP jarak jauh
url: https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers
description: Hubungkan Claude ke server MCP jarak jauh pihak ketiga melalui API konektor MCP. Telusuri contoh server dan tinjau langkah-langkah untuk terhubung.
---

Beberapa perusahaan telah menerapkan "remote MCP servers" (server MCP jarak jauh) yang dapat dihubungkan oleh developer dengan menggunakan API konektor MCP Anthropic. Server-server ini memperluas kemampuan yang tersedia bagi developer dan pengguna akhir dengan menyediakan akses jarak jauh ke berbagai layanan dan alat melalui protokol MCP.

<Note>
  Server MCP jarak jauh yang tercantum di bawah ini adalah layanan pihak ketiga yang dirancang untuk bekerja dengan Claude API. Server-server ini tidak dimiliki, dioperasikan, atau didukung oleh Anthropic. Pengguna sebaiknya hanya terhubung ke server MCP jarak jauh yang mereka percayai dan sebaiknya meninjau praktik keamanan serta ketentuan setiap server sebelum terhubung.
</Note>

## Menghubungkan ke server MCP jarak jauh

Untuk terhubung ke server MCP jarak jauh:

1. Tinjau dokumentasi untuk server spesifik yang ingin Anda gunakan.
2. Pastikan Anda memiliki kredensial autentikasi yang diperlukan.
3. Ikuti petunjuk koneksi khusus server yang disediakan oleh masing-masing perusahaan.

Untuk informasi lebih lanjut tentang penggunaan server MCP jarak jauh dengan Claude API, lihat [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector).

<Note>
  Setelah terhubung, alat MCP jarak jauh mengikuti perilaku pemicuan yang sama seperti alat lainnya. Lihat [Kapan Claude menggunakan alat MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#when-claude-uses-mcp-tools).
</Note>

## Contoh server MCP jarak jauh

<MCPServersTable platform="mcpConnector" />

<Note>
  **Mencari lebih banyak?** [Temukan ratusan server MCP lainnya di GitHub](https://github.com/modelcontextprotocol/servers).
</Note>
