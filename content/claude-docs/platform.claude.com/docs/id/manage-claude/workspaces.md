---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/workspaces
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 6371dc4a397694b67b83dae78b4bbed96830a5acd42044df59912d3fd98e6031
---

# Workspace

Atur kunci API, kelola akses tim, dan kendalikan biaya dengan workspace.

---

Workspace menyediakan cara untuk mengatur penggunaan API Anda dalam sebuah organisasi. Gunakan workspace untuk memisahkan proyek, lingkungan, atau tim yang berbeda sambil tetap mempertahankan penagihan dan administrasi terpusat.

## Cara kerja workspace

Setiap organisasi memiliki **Default Workspace** yang tidak dapat diganti namanya, diarsipkan, atau dihapus. Saat Anda membuat workspace tambahan, Anda dapat menetapkan kunci API, anggota, dan batas sumber daya untuk masing-masing workspace.

Karakteristik utama:

* **Pengidentifikasi workspace** menggunakan prefiks `wrkspc_` (misalnya, `wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ`)
* **Maksimum 100 workspace** per organisasi (workspace yang diarsipkan tidak dihitung)
* **Default Workspace** tidak memiliki ID dan tidak muncul di endpoint daftar
* **Kunci API** dibatasi cakupannya pada satu workspace dan hanya dapat mengakses sumber daya dalam workspace tersebut

### Workspace Claude Code

Ketika anggota organisasi Anda pertama kali masuk ke [Claude Code](https://docs.claude.com/id/docs/claude-code/overview) dengan akun Claude Console mereka, Anthropic secara otomatis membuat workspace **Claude Code** di organisasi tersebut dan menambahkan anggota itu ke dalamnya. Setiap anggota berikutnya yang masuk ke Claude Code akan ditambahkan dengan cara yang sama.

Workspace Claude Code memisahkan lalu lintas Claude Code dari beban kerja API Anda yang lain:

* Claude Code membuat kunci API per pengguna di workspace ini saat masuk. Anda tidak dapat membuat kunci di dalamnya secara manual dari Console.
* Kunci Claude Code berhenti berfungsi jika pemiliknya dihapus dari workspace atau organisasi, tidak seperti kunci workspace standar.
* Penggunaan Claude Code memiliki batas laju terpisah, dan admin dapat membatasi porsinya dari batas organisasi di [Settings > Workspaces](/settings/workspaces).
* Ini adalah satu-satunya workspace yang mendukung batas pengeluaran bulanan per pengguna.

<Warning>
  Mengarsipkan workspace Claude Code akan menonaktifkan proses masuk Claude Code melalui penagihan Console untuk seluruh organisasi.
</Warning>

## Peran dan izin workspace

Anggota dapat memiliki peran yang berbeda di setiap workspace, memungkinkan kontrol akses yang terperinci.

| Peran                       | Izin                                                                                                                 |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Workspace User              | Hanya menggunakan Workbench                                                                                          |
| Workspace Limited Developer | Membuat dan mengelola kunci API, menggunakan API. Tidak dapat mengakses tampilan pelacakan sesi atau mengunduh file. |
| Workspace Developer         | Membuat dan mengelola kunci API, menggunakan API                                                                     |
| Workspace Admin             | Kontrol penuh atas pengaturan dan anggota workspace                                                                  |
| Workspace Billing           | Melihat informasi penagihan workspace (diwarisi dari peran penagihan organisasi)                                     |

### Pewarisan peran

* **Admin organisasi** secara otomatis menerima akses Workspace Admin ke semua workspace
* **Anggota penagihan organisasi** secara otomatis menerima akses Workspace Billing ke semua workspace
* **Pengguna dan developer organisasi** harus ditambahkan secara eksplisit ke setiap workspace

<Note>
  Peran Workspace Billing tidak dapat ditetapkan secara manual. Peran ini diwarisi dari kepemilikan peran penagihan organisasi.
</Note>

## Mengelola workspace

<Note>
  Hanya admin organisasi yang dapat membuat workspace. Pengguna dan developer organisasi harus ditambahkan ke workspace oleh admin.
</Note>

### Menggunakan Console

Buat dan kelola workspace di [Claude Console](/settings/workspaces).

#### Membuat workspace

<Steps>
  <Step title="Buka pengaturan workspace">
    Di Claude Console, buka **Settings > Workspaces**.
  </Step>

  <Step title="Buat workspace">
    Klik **Create workspace**.
  </Step>

  <Step title="Konfigurasikan workspace">
    Masukkan nama workspace dan pilih warna untuk identifikasi visual.
  </Step>

  <Step title="Buat workspace">
    Klik **Create** untuk menyelesaikan.
  </Step>
</Steps>

<Tip>
  Untuk beralih antar workspace di Console, gunakan pemilih **Workspaces** di sudut kiri atas.
</Tip>

#### Mengedit detail workspace

Untuk mengubah nama atau warna workspace:

1. Pilih workspace dari daftar
2. Klik menu elipsis (**...**) dan pilih **Edit details**
3. Perbarui nama atau warna dan simpan perubahan Anda

<Note>
  Default Workspace tidak dapat diganti namanya atau dihapus.
</Note>

#### Menambahkan anggota ke workspace

1. Buka tab **Members** di workspace tersebut
2. Klik **Add to Workspace**
3. Pilih anggota organisasi dan tetapkan [peran workspace](#workspace-roles-and-permissions) untuk mereka
4. Konfirmasi penambahan

Untuk menghapus anggota, klik ikon tempat sampah di samping nama mereka.

<Note>
  Admin organisasi dan anggota penagihan tidak dapat dihapus dari workspace selama mereka memegang peran organisasi tersebut.
</Note>

#### Mengatur batas workspace

Di tab **Limits**, Anda dapat mengonfigurasi:

* **Batas laju:** Tetapkan batas per tingkat model untuk permintaan per menit, token input, atau token output
* **Notifikasi pengeluaran:** Konfigurasikan peringatan saat pengeluaran mencapai ambang batas tertentu

#### Mengarsipkan workspace

Untuk mengarsipkan workspace, klik menu elipsis (**...**) dan pilih **Archive**. Pengarsipan:

* Mempertahankan data historis untuk pelaporan
* Menonaktifkan workspace dan semua kunci API yang terkait
* Tidak dapat dibatalkan

<Warning>
  Mengarsipkan workspace akan langsung mencabut semua kunci API di workspace tersebut. Tindakan ini tidak dapat dibatalkan. Jika Anda mengarsipkan [workspace Claude Code](#claude-code-workspace), anggota organisasi Anda tidak dapat lagi masuk ke Claude Code melalui penagihan Console.
</Warning>

### Menggunakan Admin API

Kelola workspace secara terprogram menggunakan [Admin API](/docs/id/manage-claude/admin-api).

<Note>
  Endpoint Admin API memerlukan kunci Admin API (dimulai dengan `sk-ant-admin...`) yang berbeda dari kunci API standar. Lihat [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys) untuk cara menyediakannya.
</Note>

```bash cURL
# Membuat workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"name": "Production"}'

# Menampilkan daftar workspace
curl "https://api.anthropic.com/v1/organizations/workspaces?limit=10&include_archived=false" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Mengarsipkan workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Workspaces](/docs/id/api/admin-api/workspaces/get-workspace).

### Mengelola anggota workspace

Tambahkan, perbarui, atau hapus anggota dari workspace:

```bash cURL
# Tambahkan anggota ke workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "user_id": "user_xxx",
    "workspace_role": "workspace_developer"
  }'

# Perbarui peran anggota
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"workspace_role": "workspace_admin"}'

# Hapus anggota dari workspace
curl --request DELETE "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Untuk detail parameter lengkap, lihat [referensi API Workspace Members](/docs/id/api/admin-api/workspace_members/get-workspace-member).

## Kunci API dan cakupan sumber daya

Kunci API dibatasi cakupannya pada workspace tertentu. Saat Anda membuat kunci API di sebuah workspace, kunci tersebut hanya dapat mengakses sumber daya dalam workspace itu.

Sumber daya yang dibatasi cakupannya pada workspace meliputi:

* **File** yang dibuat melalui [Files API](/docs/id/build-with-claude/files)
* **Message Batch** yang dibuat melalui [Batch API](/docs/id/build-with-claude/batch-processing)
* **Skill** yang dibuat melalui [Skills API](/docs/id/build-with-claude/skills-guide)

Beberapa sumber daya dikelola di tingkat organisasi dan tidak dapat dikelola dengan kunci API workspace:

* **[MCP tunnel](/docs/id/agents-and-tools/mcp-tunnels/overview)** dikelola dengan token OAuth bercakupan organisasi (`org:manage_tunnels`) yang diperoleh melalui [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation), bukan kunci API workspace, dan batas maksimum 10 tunnel aktif berlaku untuk seluruh organisasi. Pengelolaan tunnel memerlukan peran dengan izin pengelolaan tunnel; developer organisasi dapat melihat tetapi tidak dapat mengubahnya. Tunnel dibuat dalam sebuah workspace, dan daftar **MCP tunnels** di Console serta pemilih server Managed Agent hanya menampilkan tunnel di workspace saat ini.
* **Workspace** itu sendiri dan **anggota organisasi** dikelola melalui [Admin API](/docs/id/manage-claude/admin-api), yang memerlukan kunci Admin API.

<Note>
  [Cache prompt](/docs/id/build-with-claude/prompt-caching) juga diisolasi per workspace di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) (di mana Claude saat ini dalam versi beta). Di Amazon Bedrock dan Vertex AI, cache prompt diisolasi per organisasi.
</Note>

<Tip>
  Untuk mengambil ID workspace organisasi Anda, gunakan endpoint [List Workspaces](/docs/id/api/admin-api/workspaces/list-workspaces), atau temukan di [Claude Console](/settings/workspaces).
</Tip>

## Batas workspace

Anda dapat menetapkan batas pengeluaran dan batas laju kustom untuk setiap workspace guna melindungi dari penggunaan berlebihan dan memastikan distribusi sumber daya yang adil.

### Menetapkan batas workspace

Batas workspace dapat ditetapkan lebih rendah dari (tetapi tidak lebih tinggi dari) batas organisasi Anda:

* **Batas pengeluaran:** Membatasi pengeluaran bulanan untuk sebuah workspace
* **Batas laju:** Membatasi permintaan per menit, token input per menit, atau token output per menit

<Note>
  - Anda tidak dapat menetapkan batas pada Default Workspace
  - Jika tidak ditetapkan, batas workspace akan sama dengan batas organisasi
  - Batas tingkat organisasi selalu berlaku, meskipun jumlah batas workspace melebihinya
</Note>

Untuk informasi terperinci tentang batas laju dan cara kerjanya, lihat [Batas laju](/docs/id/api/rate-limits). Anda juga dapat membaca batas laju organisasi dan workspace Anda saat ini secara terprogram dengan [Rate Limits API](/docs/id/manage-claude/rate-limits-api).

## Pelacakan penggunaan dan biaya

Lacak penggunaan dan biaya berdasarkan workspace menggunakan [Usage and Cost API](/docs/id/manage-claude/usage-cost-api):

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
workspace_ids[]=wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ&\
group_by[]=workspace_id&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Penggunaan dan biaya yang diatribusikan ke Default Workspace memiliki nilai `null` untuk `workspace_id`.

## Kasus penggunaan umum

### Pemisahan lingkungan

Buat workspace terpisah untuk development, staging, dan production:

| Workspace   | Tujuan                                                       |
| ----------- | ------------------------------------------------------------ |
| Development | Pengujian dan eksperimen dengan batas laju yang lebih rendah |
| Staging     | Pengujian pra-produksi dengan batas yang menyerupai produksi |
| Production  | Lalu lintas langsung dengan batas laju penuh dan pemantauan  |

### Isolasi tim atau departemen

Tetapkan workspace ke tim yang berbeda untuk alokasi biaya dan kontrol akses:

* **Tim engineering** dengan akses developer
* **Tim data science** dengan kunci API mereka sendiri
* **Tim support** dengan akses terbatas untuk alat pelanggan

### Pengorganisasian berbasis proyek

Buat workspace untuk proyek atau produk tertentu guna melacak penggunaan dan biaya secara terpisah.

## Praktik terbaik

<Steps>
  <Step title="Rencanakan struktur workspace Anda">
    Pertimbangkan bagaimana Anda akan mengatur workspace sebelum membuatnya. Pikirkan kebutuhan penagihan, kontrol akses, dan pelacakan penggunaan.
  </Step>

  <Step title="Gunakan nama yang bermakna">
    Beri nama workspace dengan jelas untuk menunjukkan tujuannya (misalnya, "Production - Customer Chatbot", "Dev - Internal Tools").
  </Step>

  <Step title="Tetapkan batas yang sesuai">
    Konfigurasikan batas pengeluaran dan batas laju untuk mencegah biaya tak terduga dan memastikan distribusi sumber daya yang adil.
  </Step>

  <Step title="Audit akses secara berkala">
    Tinjau keanggotaan workspace secara berkala untuk memastikan hanya pengguna yang tepat yang memiliki akses.
  </Step>

  <Step title="Pantau penggunaan">
    Gunakan [Usage and Cost API](/docs/id/manage-claude/usage-cost-api) untuk melacak konsumsi di tingkat workspace.
  </Step>
</Steps>

## FAQ

<AccordionGroup>
  <Accordion title="Apa itu Default Workspace?">
    Setiap organisasi memiliki "Default Workspace" yang tidak dapat diedit, diganti namanya, atau dihapus. Workspace ini tidak memiliki ID dan tidak muncul di endpoint daftar workspace. Penggunaan yang diatribusikan ke Default Workspace menampilkan nilai `null` untuk `workspace_id` dalam respons API.
  </Accordion>

  <Accordion title="Apa itu workspace Claude Code?">
    Anthropic membuat workspace Claude Code secara otomatis saat pertama kali anggota organisasi Anda masuk ke Claude Code dengan akun Console mereka. Workspace ini mengisolasi kunci API, penggunaan, dan batas laju Claude Code dari beban kerja Anda yang lain. Lihat [Workspace Claude Code](#claude-code-workspace) untuk detailnya.
  </Accordion>

  <Accordion title="Apakah ada batasan pada workspace?">
    Ya, Anda dapat memiliki maksimum 100 workspace per organisasi. Workspace yang diarsipkan tidak dihitung dalam batas ini.
  </Accordion>

  <Accordion title="Bagaimana peran organisasi memengaruhi akses workspace?">
    Admin organisasi secara otomatis mendapatkan peran Workspace Admin di semua workspace. Anggota penagihan organisasi secara otomatis mendapatkan peran Workspace Billing. Pengguna dan developer organisasi harus ditambahkan secara manual ke setiap workspace.
  </Accordion>

  <Accordion title="Peran apa saja yang dapat ditetapkan di workspace?">
    Pengguna dan developer organisasi dapat diberi peran Workspace Admin, Workspace Developer, Workspace Limited Developer, atau Workspace User. Peran Workspace Billing tidak dapat ditetapkan secara manual; peran ini diwarisi dari kepemilikan peran `billing` organisasi.
  </Accordion>

  <Accordion title="Apakah peran workspace admin organisasi atau anggota penagihan dapat diubah?">
    Admin organisasi dan anggota penagihan tidak dapat diubah peran workspace-nya atau dihapus dari workspace selama mereka memegang peran organisasi tersebut (dengan satu pengecualian: anggota penagihan dapat ditingkatkan ke peran Workspace Admin). Untuk semua orang lain yang tercakup dalam batasan ini, ubah peran organisasi mereka terlebih dahulu untuk mengubah akses workspace mereka.
  </Accordion>

  <Accordion title="Apa yang terjadi pada akses workspace saat peran organisasi berubah?">
    Jika admin organisasi atau anggota penagihan diturunkan menjadi pengguna atau developer, mereka kehilangan akses ke semua workspace kecuali yang perannya ditetapkan secara manual. Saat pengguna dipromosikan ke peran admin atau penagihan, mereka mendapatkan akses otomatis ke semua workspace.
  </Accordion>

  <Accordion title="Apa yang terjadi pada kunci API saat pengguna dihapus dari workspace?">
    Kunci API tetap dalam kondisi saat ini karena cakupannya adalah organisasi dan workspace, bukan pengguna individu. Pengecualiannya adalah [workspace Claude Code](#claude-code-workspace), di mana setiap kunci terikat pada anggota yang membuatnya dan berhenti berfungsi saat anggota tersebut dihapus.
  </Accordion>
</AccordionGroup>

## Lihat juga

* [Admin API](/docs/id/manage-claude/admin-api)
* [Referensi Admin API](/docs/id/api/admin)
* [Batas laju](/docs/id/api/rate-limits)
* [Usage and Cost API](/docs/id/manage-claude/usage-cost-api)
