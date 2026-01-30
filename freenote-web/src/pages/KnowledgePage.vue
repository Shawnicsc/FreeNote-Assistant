<template>
  <div class="h-full flex items-center justify-center bg-[#f5f5f7] p-8">
    <div class="max-w-2xl w-full apple-card p-12 text-center">
      <div class="w-20 h-20 bg-[#0071e3]/10 rounded-2xl flex items-center justify-center mx-auto mb-6">
        <Library class="w-10 h-10 text-[#0071e3]" />
      </div>
      <h2 class="text-3xl font-bold tracking-tight text-[#1d1d1f] mb-4">知识库</h2>
      <p class="text-lg text-[#86868b] mb-8">这里是您的个人知识中心。即将推出智能问答与知识关联功能。</p>
      <button class="apple-button-primary px-8">探索更多</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Library } from 'lucide-vue-next'
</script>
