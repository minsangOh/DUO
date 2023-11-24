<template>
  <div class="marg">
    <h5>{{ article.id }}</h5>
    <p>제목: {{ article.title }}</p>
    <p>내용: {{ article.content }}</p>
    <RouterLink :to="{ name: 'detail', params: { id: article.id }}">
    </RouterLink>
    <hr>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object
})
</script>

<style scoped>
.marg {
  margin: 3%;
}
</style>
