<template>
  <div class="mermaid-wrapper flex flex-col items-center w-full">
    <div 
      ref="mermaidRef" 
      class="mermaid bg-white p-4 rounded-xl w-full flex justify-center min-h-[100px]"
    >
      {{ code }}
    </div>
    <div v-if="error" class="text-red-500 text-xs mt-2 p-2 bg-red-50 rounded border border-red-100">
      渲染错误: {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import mermaid from 'mermaid'

const props = defineProps<{
  code: string
}>()

const mermaidRef = ref<HTMLElement | null>(null)
const error = ref<string | null>(null)

const renderMermaid = async () => {
  if (!mermaidRef.value || !props.code) return
  
  error.value = null
  
  // 核心：清空并设置原始代码，移除已处理标记
  mermaidRef.value.innerHTML = props.code
  mermaidRef.value.removeAttribute('data-processed')
  
  try {
    await nextTick()
    await mermaid.run({
      nodes: [mermaidRef.value]
    })
  } catch (e: any) {
    console.error('Mermaid render error:', e)
    error.value = e.message || '语法解析错误'
  }
}

onMounted(() => {
  mermaid.initialize({ 
    startOnLoad: false, 
    theme: 'default',
    securityLevel: 'loose',
    fontFamily: 'SF Pro Text, Inter, system-ui'
  })
  renderMermaid()
})

watch(() => props.code, renderMermaid)
</script>

<style scoped>
.mermaid-container {
  min-height: 200px;
  background: white;
  border-radius: 12px;
}
</style>
