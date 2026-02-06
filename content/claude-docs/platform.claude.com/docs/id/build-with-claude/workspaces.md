---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/workspaces
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 850c4d16dcdb4e44195c2fa9b2ae7d0323344c849b9256e4e087d3f7382ad79a
---

# Ruang Kerja

Atur kunci API, kelola akses tim, dan kontrol biaya dengan ruang kerja.

---

Ruang kerja menyediakan cara untuk mengatur penggunaan API Anda dalam organisasi. Gunakan ruang kerja untuk memisahkan proyek, lingkungan, atau tim yang berbeda sambil mempertahankan penagihan dan administrasi terpusat.

## Cara kerja ruang kerja

Setiap organisasi memiliki **Ruang Kerja Default** yang tidak dapat diubah nama, diarsipkan, atau dihapus. Ketika Anda membuat ruang kerja tambahan, Anda dapat menetapkan kunci API, anggota, dan batas sumber daya untuk masing-masing.

Karakteristik utama:
- **Pengenal ruang kerja** menggunakan awalan `wrkspc_` (misalnya, `wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ`)
- **Maksimal 100 ruang kerja** per organisasi (ruang kerja yang diarsipkan tidak dihitung)
- **Ruang Kerja Default** tidak memiliki ID dan tidak muncul di endpoint daftar
- **Kunci API** dibatasi pada satu ruang kerja dan hanya dapat mengakses sumber daya dalam ruang kerja tersebut

## Peran dan izin ruang kerja

Anggota dapat memiliki peran berbeda di setiap ruang kerja, memungkinkan kontrol akses yang terperinci.

| Peran | Izin |
|------|-------------|
| Pengguna Ruang Kerja | Gunakan Workbench saja |
| Pengembang Ruang Kerja | Buat dan kelola kunci API, gunakan API |
| Admin Ruang Kerja | Kontrol penuh atas pengaturan dan anggota ruang kerja |
| Penagihan Ruang Kerja | Lihat informasi penagihan ruang kerja (diwarisi dari peran penagihan organisasi) |

### Pewarisan peran

- **Admin organisasi** secara otomatis menerima akses Admin Ruang Kerja ke semua ruang kerja
- **Anggota penagihan organisasi** secara otomatis menerima akses Penagihan Ruang Kerja ke semua ruang kerja
- **Pengguna dan pengembang organisasi** harus ditambahkan secara eksplisit ke setiap ruang kerja

<Note>
Peran Penagihan Ruang Kerja tidak dapat ditetapkan secara manual. Peran ini diwarisi dari memiliki peran penagihan organisasi.
</Note>

## Mengelola ruang kerja

<Note>
Hanya admin organisasi yang dapat membuat ruang kerja. Pengguna dan pengembang organisasi harus ditambahkan ke ruang kerja oleh admin.
</Note>

### Melalui Konsol

Buat dan kelola ruang kerja di [Konsol Claude](/settings/workspaces).

#### Buat ruang kerja

<Steps>
  <Step title="Buka pengaturan ruang kerja">
    Di Konsol Claude, buka **Pengaturan > Ruang Kerja**.
  </Step>
  <Step title="Tambahkan ruang kerja baru">
    Klik **Tambah Ruang Kerja**.
  </Step>
  <Step title="Konfigurasi ruang kerja">
    Masukkan nama ruang kerja dan pilih warna untuk identifikasi visual.
  </Step>
  <Step title="Buat ruang kerja">
    Klik **Buat** untuk menyelesaikan.
  </Step>
</Steps>

<Tip>
Untuk beralih antar ruang kerja di Konsol, gunakan pemilih **Ruang Kerja** di sudut kiri atas.
</Tip>

#### Edit detail ruang kerja

Untuk mengubah nama atau warna ruang kerja:

1. Pilih ruang kerja dari daftar
2. Klik menu elipsis (**...**) dan pilih **Edit detail**
3. Perbarui nama atau warna dan simpan perubahan Anda

<Note>
Ruang Kerja Default tidak dapat diubah nama atau dihapus.
</Note>

#### Tambahkan anggota ke ruang kerja

1. Navigasi ke tab **Anggota** ruang kerja
2. Klik **Tambah ke Ruang Kerja**
3. Pilih anggota organisasi dan tetapkan mereka [peran ruang kerja](#workspace-roles-and-permissions)
4. Konfirmasi penambahan

Untuk menghapus anggota, klik ikon tempat sampah di sebelah nama mereka.

<Note>
Admin organisasi dan anggota penagihan tidak dapat dihapus dari ruang kerja saat mereka memiliki peran organisasi tersebut.
</Note>

#### Atur batas ruang kerja

Di tab **Batas**, Anda dapat mengonfigurasi:

- **Batas laju**: Atur batas per tingkat model untuk permintaan per menit, token input, atau token output
- **Notifikasi pengeluaran**: Konfigurasikan peringatan ketika pengeluaran mencapai ambang batas tertentu

#### Arsipkan ruang kerja

Untuk mengarsipkan ruang kerja, klik menu elipsis (**...**) dan pilih **Arsipkan**. Pengarsipan:

- Menyimpan data historis untuk pelaporan
- Menonaktifkan ruang kerja dan semua kunci API terkait
- Tidak dapat dibatalkan

<Warning>
Mengarsipkan ruang kerja segera mencabut semua kunci API di ruang kerja tersebut. Tindakan ini tidak dapat dibatalkan.
</Warning>

### Melalui Admin API

Kelola ruang kerja secara terprogram menggunakan [Admin API](/docs/id/build-with-claude/administration-api).

<Note>
Endpoint Admin API memerlukan kunci Admin API (dimulai dengan `sk-ant-admin...`) yang berbeda dari kunci API standar. Hanya anggota organisasi dengan peran admin yang dapat menyediakan kunci Admin API melalui [Konsol Claude](/settings/admin-keys).
</Note>

```bash
# Create a workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"name": "Production"}'

# List workspaces
curl "https://api.anthropic.com/v1/organizations/workspaces?limit=10&include_archived=false" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Archive a workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Ruang Kerja](/docs/id/api/admin-api/workspaces/get-workspace).

### Mengelola anggota ruang kerja

Tambahkan, perbarui, atau hapus anggota dari ruang kerja:

```bash
# Add a member to a workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "user_id": "user_xxx",
    "workspace_role": "workspace_developer"
  }'

# Update a member's role
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"workspace_role": "workspace_admin"}'

# Remove a member from a workspace
curl --request DELETE "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Untuk detail parameter lengkap, lihat [referensi API Anggota Ruang Kerja](/docs/id/api/admin-api/workspace_members/get-workspace-member).

## Kunci API dan cakupan sumber daya

Kunci API dibatasi pada ruang kerja tertentu. Ketika Anda membuat kunci API di ruang kerja, kunci tersebut hanya dapat mengakses sumber daya dalam ruang kerja tersebut.

Sumber daya yang dibatasi pada ruang kerja meliputi:
- **File** yang dibuat melalui [Files API](/docs/id/build-with-claude/files)
- **Batch Pesan** yang dibuat melalui [Batch API](/docs/id/build-with-claude/batch-processing)
- **Keterampilan** yang dibuat melalui [Skills API](/docs/id/build-with-claude/skills-guide)

<Note>
Mulai 5 Februari 2026, [cache prompt](/docs/id/build-with-claude/prompt-caching) juga akan diisolasi per ruang kerja (berlaku untuk Claude API dan Azure saja).
</Note>

<Tip>
Untuk mengambil ID ruang kerja organisasi Anda, gunakan endpoint [Daftar Ruang Kerja](/docs/id/api/admin-api/workspaces/list-workspaces), atau temukan di [Konsol Claude](/settings/workspaces).
</Tip>

## Batas ruang kerja

Anda dapat menetapkan batas pengeluaran dan laju kustom untuk setiap ruang kerja untuk melindungi dari penggunaan berlebihan dan memastikan distribusi sumber daya yang adil.

### Menetapkan batas ruang kerja

Batas ruang kerja dapat ditetapkan lebih rendah dari (tetapi tidak lebih tinggi dari) batas organisasi Anda:

- **Batas pengeluaran**: Batasi pengeluaran bulanan untuk ruang kerja
- **Batas laju**: Batasi permintaan per menit, token input per menit, atau token output per menit

<Note>
- Anda tidak dapat menetapkan batas pada Ruang Kerja Default
- Jika tidak ditetapkan, batas ruang kerja cocok dengan batas organisasi
- Batas di seluruh organisasi selalu berlaku, bahkan jika batas ruang kerja ditambahkan melebihi
</Note>

Untuk informasi terperinci tentang batas laju dan cara kerjanya, lihat [Batas laju](/docs/id/api/rate-limits).

## Pelacakan penggunaan dan biaya

Lacak penggunaan dan biaya berdasarkan ruang kerja menggunakan [Usage and Cost API](/docs/id/build-with-claude/usage-cost-api):

```bash
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
workspace_ids[]=wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ&\
group_by[]=workspace_id&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ADMIN_API_KEY"
```

Penggunaan dan biaya yang dikaitkan dengan Ruang Kerja Default memiliki nilai `null` untuk `workspace_id`.

## Kasus penggunaan umum

### Pemisahan lingkungan

Buat ruang kerja terpisah untuk pengembangan, staging, dan produksi:

| Ruang Kerja | Tujuan |
|-----------|---------|
| Pengembangan | Pengujian dan eksperimen dengan batas laju yang lebih rendah |
| Staging | Pengujian pra-produksi dengan batas seperti produksi |
| Produksi | Lalu lintas langsung dengan batas laju penuh dan pemantauan |

### Isolasi tim atau departemen

Tetapkan ruang kerja ke tim berbeda untuk alokasi biaya dan kontrol akses:

- **Tim teknik** dengan akses pengembang
- **Tim ilmu data** dengan kunci API mereka sendiri
- **Tim dukungan** dengan akses terbatas untuk alat pelanggan

### Organisasi berbasis proyek

Buat ruang kerja untuk proyek atau produk tertentu untuk melacak penggunaan dan biaya secara terpisah.

## Praktik terbaik

<Steps>
  <Step title="Rencanakan struktur ruang kerja Anda">
    Pertimbangkan bagaimana Anda akan mengatur ruang kerja sebelum membuatnya. Pikirkan tentang penagihan, kontrol akses, dan kebutuhan pelacakan penggunaan.
  </Step>
  <Step title="Gunakan nama yang bermakna">
    Beri nama ruang kerja dengan jelas untuk menunjukkan tujuannya (misalnya, "Produksi - Chatbot Pelanggan", "Dev - Alat Internal").
  </Step>
  <Step title="Atur batas yang sesuai">
    Konfigurasikan batas pengeluaran dan laju untuk mencegah biaya yang tidak terduga dan memastikan distribusi sumber daya yang adil.
  </Step>
  <Step title="Audit akses secara teratur">
    Tinjau keanggotaan ruang kerja secara berkala untuk memastikan hanya pengguna yang sesuai yang memiliki akses.
  </Step>
  <Step title="Pantau penggunaan">
    Gunakan [Usage and Cost API](/docs/id/build-with-claude/usage-cost-api) untuk melacak konsumsi tingkat ruang kerja.
  </Step>
</Steps>

## FAQ

<section title="Apa itu Ruang Kerja Default?">

Setiap organisasi memiliki "Ruang Kerja Default" yang tidak dapat diedit, diubah nama, atau dihapus. Ruang kerja ini tidak memiliki ID dan tidak muncul di endpoint daftar ruang kerja. Penggunaan yang dikaitkan dengan Ruang Kerja Default menunjukkan nilai `null` untuk `workspace_id` dalam respons API.

</section>

<section title="Apakah ada batasan pada ruang kerja?">

Ya, Anda dapat memiliki maksimal 100 ruang kerja per organisasi. Ruang kerja yang diarsipkan tidak dihitung terhadap batas ini.

</section>

<section title="Bagaimana peran organisasi mempengaruhi akses ruang kerja?">

Admin organisasi secara otomatis mendapatkan peran Admin Ruang Kerja di semua ruang kerja. Anggota penagihan organisasi secara otomatis mendapatkan peran Penagihan Ruang Kerja. Pengguna dan pengembang organisasi harus ditambahkan secara manual ke setiap ruang kerja.

</section>

<section title="Peran mana yang dapat ditetapkan di ruang kerja?">

Pengguna dan pengembang organisasi dapat ditetapkan peran Admin Ruang Kerja, Pengembang Ruang Kerja, atau Pengguna Ruang Kerja. Peran Penagihan Ruang Kerja tidak dapat ditetapkan secara manual; peran ini diwarisi dari memiliki peran `billing` organisasi.

</section>

<section title="Dapatkah peran ruang kerja admin atau anggota penagihan organisasi diubah?">

Hanya anggota penagihan organisasi yang dapat memiliki peran ruang kerja mereka ditingkatkan ke peran admin. Jika tidak, admin organisasi dan anggota penagihan tidak dapat memiliki peran ruang kerja mereka diubah atau dihapus dari ruang kerja saat mereka memiliki peran organisasi tersebut. Akses ruang kerja mereka harus dimodifikasi dengan mengubah peran organisasi mereka terlebih dahulu.

</section>

<section title="Apa yang terjadi pada akses ruang kerja ketika peran organisasi berubah?">

Jika admin organisasi atau anggota penagihan diturunkan menjadi pengguna atau pengembang, mereka kehilangan akses ke semua ruang kerja kecuali yang mereka tetapkan peran secara manual. Ketika pengguna dipromosikan ke peran admin atau penagihan, mereka mendapatkan akses otomatis ke semua ruang kerja.

</section>

<section title="Apa yang terjadi pada kunci API ketika pengguna dihapus dari ruang kerja?">

Kunci API tetap dalam keadaan saat ini karena mereka dibatasi pada organisasi dan ruang kerja, bukan pada pengguna individual.

</section>

## Lihat juga

- [Gambaran umum Admin API](/docs/id/build-with-claude/administration-api)
- [Referensi Admin API](/docs/id/api/admin)
- [Batas laju](/docs/id/api/rate-limits)
- [Usage and Cost API](/docs/id/build-with-claude/usage-cost-api)