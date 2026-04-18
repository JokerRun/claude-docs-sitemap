---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/eval-tool
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 71efead303e9cd9ec055d8562c72ff4bc3e01d81e99c8110641e844794cdb393
---

# Menggunakan Alat Evaluasi

Claude Console menampilkan **Alat Evaluasi** yang memungkinkan Anda menguji prompt Anda dalam berbagai skenario.

---

## Mengakses Fitur Evaluasi

Untuk memulai dengan alat Evaluasi:

1. Buka Claude Console dan navigasikan ke editor prompt.
2. Setelah menyusun prompt Anda, cari tab 'Evaluate' di bagian atas layar.

![Mengakses Fitur Evaluasi](/docs/images/access_evaluate.png)

<Tip>
Pastikan prompt Anda mencakup setidaknya 1-2 variabel dinamis menggunakan sintaks kurung kurawal ganda: \{\{variable\}\}. Ini diperlukan untuk membuat set tes eval.
</Tip>

## Menghasilkan Prompt

Console menawarkan [pembuat prompt](/docs/id/build-with-claude/prompt-engineering/prompting-tools) bawaan yang didukung oleh Claude Opus 4.1:

<Steps>
  <Step title="Klik 'Generate Prompt'">
    Mengklik alat pembantu 'Generate Prompt' akan membuka modal yang memungkinkan Anda memasukkan informasi tugas Anda.
  </Step>
  <Step title="Jelaskan tugas Anda">
    Jelaskan tugas yang diinginkan (misalnya, "Triage permintaan dukungan pelanggan masuk") dengan detail sebanyak atau sesedikit yang Anda inginkan. Semakin banyak konteks yang Anda sertakan, semakin banyak Claude dapat menyesuaikan prompt yang dihasilkan dengan kebutuhan spesifik Anda.
  </Step>
  <Step title="Hasilkan prompt Anda">
    Mengklik tombol 'Generate Prompt' oranye di bagian bawah akan membuat Claude menghasilkan prompt berkualitas tinggi untuk Anda. Anda kemudian dapat meningkatkan prompt tersebut menggunakan layar Evaluasi di Console.
  </Step>
</Steps>

Fitur ini memudahkan untuk membuat prompt dengan sintaks variabel yang sesuai untuk evaluasi.

![Pembuat Prompt](/docs/images/promptgenerator.png)

## Membuat Kasus Uji

Ketika Anda mengakses layar Evaluasi, Anda memiliki beberapa opsi untuk membuat kasus uji:

1. Klik tombol '+ Add Row' di bagian bawah kiri untuk menambahkan kasus secara manual.
2. Gunakan fitur 'Generate Test Case' untuk membuat Claude secara otomatis menghasilkan kasus uji untuk Anda.
3. Impor kasus uji dari file CSV.

Untuk menggunakan fitur 'Generate Test Case':

<Steps>
  <Step title="Klik pada 'Generate Test Case'">
    Claude akan menghasilkan kasus uji untuk Anda, satu baris setiap kali Anda mengklik tombol.
  </Step>
  <Step title="Edit logika generasi (opsional)">
    Anda juga dapat mengedit logika generasi kasus uji dengan mengklik panah dropdown di sebelah kanan tombol 'Generate Test Case', kemudian pada 'Show generation logic' di bagian atas jendela Variabel yang muncul. Anda mungkin harus mengklik `Generate' di bagian atas kanan jendela ini untuk mengisi logika generasi awal.

    Mengedit ini memungkinkan Anda menyesuaikan dan menyempurnakan kasus uji yang dihasilkan Claude dengan presisi dan spesifisitas yang lebih besar.
  </Step>
</Steps>

Berikut adalah contoh layar Evaluasi yang terisi dengan beberapa kasus uji:

![Layar Evaluasi Terisi](/docs/images/eval_populated.png)

<Note>
Jika Anda memperbarui teks prompt asli Anda, Anda dapat menjalankan kembali seluruh suite eval terhadap prompt baru untuk melihat bagaimana perubahan mempengaruhi kinerja di semua kasus uji.
</Note>

## Tips untuk Evaluasi yang Efektif

<section title="Struktur Prompt untuk Evaluasi">

Untuk memanfaatkan alat Evaluasi sebaik-baiknya, struktur prompt Anda dengan format input dan output yang jelas. Misalnya:

```text
Dalam tugas ini, Anda akan menghasilkan cerita satu kalimat yang lucu yang menggabungkan dua elemen: warna dan suara.
Warna yang akan disertakan dalam cerita adalah:
<color>
{{COLOR}}
</color>
Suara yang akan disertakan dalam cerita adalah:
<sound>
{{SOUND}}
</sound>
Berikut adalah langkah-langkah untuk menghasilkan cerita:
1. Pikirkan tentang objek, hewan, atau pemandangan yang biasanya dikaitkan dengan warna yang diberikan. Misalnya, jika warnanya adalah "biru", Anda mungkin memikirkan langit, laut, atau burung biru.
2. Bayangkan tindakan, peristiwa, atau pemandangan sederhana yang melibatkan objek/hewan/pemandangan berwarna yang Anda identifikasi dan suara yang diberikan. Misalnya, jika warnanya adalah "biru" dan suaranya adalah "peluit", Anda mungkin membayangkan burung biru yang bersiul melodi.
3. Jelaskan tindakan, peristiwa, atau pemandangan yang Anda bayangkan dalam satu kalimat yang ringkas. Fokus pada membuat kalimat itu lucu, membangkitkan emosi, dan imajinatif. Misalnya: "Seekor burung biru yang ceria bersiul melodi meriah saat terbang melintasi langit biru."
Harap pertahankan cerita Anda hanya satu kalimat. Bertujuan untuk membuat kalimat itu secharming dan engaging mungkin sambil secara alami menggabungkan warna dan suara yang diberikan.
Tulis cerita satu kalimat yang sudah selesai Anda buat di dalam tag <story>.

```

Struktur ini memudahkan untuk memvariasikan input (\{\{COLOR\}\} dan \{\{SOUND\}\}) dan mengevaluasi output secara konsisten.

</section>

<Tip>
Gunakan alat pembantu 'Generate a prompt' di Console untuk dengan cepat membuat prompt dengan sintaks variabel yang sesuai untuk evaluasi.
</Tip>

## Memahami dan membandingkan hasil

Alat Evaluasi menawarkan beberapa fitur untuk membantu Anda menyempurnakan prompt Anda:

1. **Perbandingan berdampingan**: Bandingkan output dari dua atau lebih prompt untuk dengan cepat melihat dampak perubahan Anda.
2. **Penilaian kualitas**: Nilai kualitas respons pada skala 5 poin untuk melacak peningkatan kualitas respons per prompt.
3. **Versioning prompt**: Buat versi baru prompt Anda dan jalankan kembali suite tes untuk dengan cepat melakukan iterasi dan meningkatkan hasil.

Dengan meninjau hasil di seluruh kasus uji dan membandingkan versi prompt yang berbeda, Anda dapat mendeteksi pola dan membuat penyesuaian yang tepat pada prompt Anda dengan lebih efisien.

Mulai evaluasi prompt Anda hari ini untuk membangun aplikasi AI yang lebih robust dengan Claude!