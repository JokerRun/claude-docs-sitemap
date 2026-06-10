---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: e9ac2a6c5384b14b0abdf5bdb19bfedb9b62a503e9b7fbed3bda39e5ecd53b25
---

# Server MCP jarak jauh

---

Beberapa perusahaan telah menerapkan server MCP jarak jauh yang dapat dihubungkan oleh pengembang melalui API konektor MCP Anthropic. Server-server ini memperluas kemampuan yang tersedia bagi pengembang dan pengguna akhir dengan menyediakan akses jarak jauh ke berbagai layanan dan alat melalui protokol MCP.

<Note>
    Server MCP jarak jauh yang tercantum di bawah ini adalah layanan pihak ketiga yang dirancang untuk bekerja dengan API Claude. Server-server
    ini tidak dimiliki, dioperasikan, atau didukung oleh Anthropic. Pengguna sebaiknya hanya terhubung ke server MCP jarak jauh yang mereka percaya dan
    sebaiknya meninjau praktik keamanan serta ketentuan setiap server sebelum terhubung.
</Note>

## Menghubungkan ke server MCP jarak jauh \{#connecting-to-remote-mcp-servers}

Untuk terhubung ke server MCP jarak jauh:

1. Tinjau dokumentasi untuk server spesifik yang ingin Anda gunakan.
2. Pastikan Anda memiliki kredensial autentikasi yang diperlukan.
3. Ikuti instruksi koneksi spesifik server yang disediakan oleh masing-masing perusahaan.

Untuk informasi lebih lanjut tentang penggunaan server MCP jarak jauh dengan API Claude, lihat [dokumentasi konektor MCP](/docs/id/agents-and-tools/mcp-connector).

<Note>
Setelah terhubung, alat MCP jarak jauh mengikuti perilaku pemicuan yang sama seperti alat lainnya. Lihat [Kapan Claude menggunakan alat MCP](/docs/id/agents-and-tools/mcp-connector#when-claude-uses-mcp-tools).
</Note>

## Contoh server MCP jarak jauh \{#remote-mcp-server-examples}

<MCPServersTable platform="mcpConnector" />

<Note>
**Mencari lebih banyak?** [Temukan ratusan server MCP lainnya di GitHub](https://github.com/modelcontextprotocol/servers).
</Note>