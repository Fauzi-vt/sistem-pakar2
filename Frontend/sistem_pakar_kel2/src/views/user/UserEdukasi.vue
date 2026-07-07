<template>
  <UserLayout>
    <AppBreadcrumb :items="[{ label: 'Dashboard', to: '/user/dashboard' }, { label: 'Tentang Sistem' }]" />
    <PageHeader 
      title="Edukasi & Informasi" 
      description="Pelajari lebih lanjut mengenai penyakit THT, cara menjaga kesehatan, dan informasi penting lainnya." 
    />

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pb-8">
      
      <div v-for="(item, idx) in edukasiList" :key="idx" 
           class="bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm flex flex-col transition-all hover:shadow-md hover:border-outline">
        
        <!-- Header -->
        <div class="px-6 py-4 border-b border-outline-variant bg-surface-container-low flex items-center gap-3">
          <div class="w-10 h-10 rounded-full flex items-center justify-center shrink-0" :class="item.colorClass">
            <span class="material-symbols-outlined">{{ item.icon }}</span>
          </div>
          <h3 class="font-headline-sm font-bold text-primary">{{ item.title }}</h3>
        </div>

        <!-- Content -->
        <div class="p-6 flex-1">
          <div class="prose prose-sm prose-p:text-on-surface-variant prose-p:leading-relaxed prose-li:text-on-surface-variant prose-headings:text-primary max-w-none" v-html="item.content"></div>
        </div>

      </div>

    </div>

    <!-- Global Medical Disclaimer -->
    <div class="bg-error-container/30 border border-error-container rounded-2xl p-6 mb-8 text-center flex flex-col items-center">
      <div class="w-12 h-12 rounded-full bg-error-container text-error flex items-center justify-center mb-4">
        <span class="material-symbols-outlined text-2xl">warning</span>
      </div>
      <h3 class="font-headline-sm font-bold text-error mb-2">Disclaimer Medis Penting</h3>
      <p class="font-body-md text-on-surface-variant max-w-2xl leading-relaxed">
        Aplikasi Sistem Pakar ini dikembangkan untuk tujuan edukasi dan skrining awal penyakit THT. 
        Aplikasi ini <strong>tidak dirancang untuk menggantikan</strong> diagnosis profesional, pemeriksaan fisik, tes laboratorium, atau saran langsung dari dokter spesialis THT. 
        Segera kunjungi rumah sakit atau fasilitas kesehatan terdekat jika Anda mengalami gejala berat yang mengganggu aktivitas sehari-hari.
      </p>
    </div>
  </UserLayout>
</template>

<script setup>
import UserLayout from '@/layouts/UserLayout.vue'
import AppBreadcrumb from '@/components/common/AppBreadcrumb.vue'
import PageHeader from '@/components/common/PageHeader.vue'

const edukasiList = [
  {
    icon: 'earbuds',
    title: 'Apa itu THT?',
    colorClass: 'bg-primary-container text-primary',
    content: `
      <p><strong>THT</strong> singkatan dari <em>Telinga, Hidung, dan Tenggorokan</em> (dalam bahasa medis: Otorhinolaryngology). Ini adalah cabang ilmu kedokteran spesialis yang mendiagnosis dan mengobati berbagai penyakit terkait tiga organ penting tersebut serta bagian leher dan kepala.</p>
      <p>Karena saluran telinga, hidung, dan tenggorokan saling terhubung melalui saluran eustachius, infeksi pada satu bagian sering kali dapat menyebar dan memengaruhi bagian lainnya.</p>
    `
  },
  {
    icon: 'coronavirus',
    title: 'Penyakit THT Umum',
    colorClass: 'bg-secondary-container text-secondary',
    content: `
      <ul class="space-y-2 list-disc pl-4 mt-2">
        <li><strong>Otitis Media:</strong> Infeksi pada telinga bagian tengah, sering menyebabkan nyeri dan demam, biasa terjadi pada anak-anak.</li>
        <li><strong>Sinusitis:</strong> Peradangan pada rongga sinus yang menghasilkan lendir dan menyebabkan hidung tersumbat, nyeri wajah, hingga sakit kepala.</li>
        <li><strong>Tonsilitis:</strong> Radang amandel yang menyebabkan nyeri saat menelan, tenggorokan merah, dan pembengkakan.</li>
        <li><strong>Faringitis:</strong> Radang tenggorokan umum yang sering disebabkan oleh infeksi virus atau bakteri.</li>
      </ul>
    `
  },
  {
    icon: 'health_and_safety',
    title: 'Tips Menjaga Kesehatan THT',
    colorClass: 'bg-tertiary-container text-tertiary',
    content: `
      <ol class="space-y-2 list-decimal pl-4 mt-2">
        <li><strong>Jangan gunakan korek kuping (cotton bud)</strong> terlalu dalam, biarkan telinga membersihkan dirinya sendiri.</li>
        <li><strong>Hindari paparan suara keras</strong> dalam waktu lama (misalnya menggunakan earphone dengan volume >60%).</li>
        <li><strong>Jaga kebersihan hidung</strong> dengan tidak mengorek hidung menggunakan tangan kotor untuk mencegah masuknya bakteri.</li>
        <li><strong>Perbanyak minum air putih hangat</strong> untuk menjaga kelembapan mukosa tenggorokan.</li>
      </ol>
    `
  },
  {
    icon: 'local_hospital',
    title: 'Kapan Harus ke Dokter?',
    colorClass: 'bg-error-container text-error',
    content: `
      <p>Segera buat janji temu dengan dokter spesialis THT jika Anda mengalami:</p>
      <ul class="space-y-2 list-disc pl-4 mt-2">
        <li>Nyeri telinga yang tajam, keluar cairan berbau, atau pendengaran tiba-tiba hilang.</li>
        <li>Hidung tersumbat parah lebih dari 10 hari, disertai lendir hijau/kuning atau darah.</li>
        <li>Sakit tenggorokan parah hingga kesulitan menelan air liur, atau suara serak menetap lebih dari 2 minggu.</li>
        <li>Sering pusing berputar (vertigo) yang parah dan tiba-tiba.</li>
      </ul>
    `
  }
]
</script>
