<template>
  <div class="marg">
    <h3>Article List</h3>
    <ArticleListItem 
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useCounterStore } from '@/stores/counter'
import ArticleListItem from '@/components/ArticleListItem.vue'

const store = useCounterStore()
onMounted(() => {
    store.getArticles();
    console.log(store.articles)
  })
</script>

<style scoped>
.marg {
  margin: 3%;
}
</style>
