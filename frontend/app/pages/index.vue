<script setup>
const features = [
  { title: 'سریع', desc: 'با Nuxt، رندر سمت سرور داری' },
  { title: 'ساده', desc: 'روتینگ فایل‌محور بدون کانفیگ' },
  { title: 'مقیاس‌پذیر', desc: 'مناسب پروژه‌های بزرگ' },
]
</script>

<template>
  <main class="home">
    <h1>به پروژه من خوش آمدید 👋</h1>
    <p>این صفحه اصلی با Nuxt ساخته شده.</p>

    <section class="features">
      <div v-for="f in features" :key="f.title" class="card">
        <h3>{{ f.title }}</h3>
        <p>{{ f.desc }}</p>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home {
  max-width: 800px;
  margin: 4rem auto;
  text-align: center;
  font-family: sans-serif;
}
.features {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}
.card {
  flex: 1;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>