<template>
  <div class="h-full bg-[#f5f5f7] flex flex-col p-6 overflow-hidden">
    <div class="max-w-4xl w-full mx-auto flex flex-col h-full">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-[#0071e3]/10 rounded-xl flex items-center justify-center">
            <Library class="w-5 h-5 text-[#0071e3]" />
          </div>
          <h2 class="text-2xl font-bold tracking-tight text-[#1d1d1f]">知识库问答</h2>
        </div>
        <button 
          @click="clearChat" 
          class="text-[13px] text-[#86868b] hover:text-[#1d1d1f] transition-colors"
        >
          清空对话
        </button>
      </div>

      <!-- Chat History -->
      <div ref="chatContainer" class="flex-1 overflow-y-auto space-y-6 mb-6 pr-2">
        <div v-if="chatHistory.length === 0" class="h-full flex flex-col items-center justify-center text-center py-20">
          <div class="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4">
            <MessageSquare class="w-8 h-8 text-[#d2d2d7]" />
          </div>
          <h3 class="text-lg font-medium text-[#1d1d1f] mb-2">欢迎使用 RAG 助手</h3>
          <p class="text-sm text-[#86868b] max-w-xs">基于您的本地 Markdown 文件，提供精准的问答支持。请输入您的问题开始对话。</p>
        </div>
        
        <div 
          v-for="(msg, index) in chatHistory" 
          :key="index"
          class="flex flex-col"
          :class="msg.role === 'user' ? 'items-end' : 'items-start'"
        >
          <div 
            class="max-w-[85%] px-4 py-3 rounded-2xl text-[15px] leading-relaxed"
            :class="msg.role === 'user' ? 'bg-[#0071e3] text-white shadow-sm' : 'bg-white text-[#1d1d1f] border border-[#d2d2d7]/30 shadow-sm'"
          >
            <div v-if="msg.role === 'assistant'" class="prose prose-sm max-w-none" v-html="renderMarkdown(msg.content)"></div>
            <div v-else>{{ msg.content }}</div>
          </div>
          <span class="text-[11px] text-[#86868b] mt-1 mx-2 uppercase tracking-wider font-medium">
            {{ msg.role === 'user' ? 'You' : 'Assistant' }}
          </span>
        </div>

        <div v-if="isLoading" class="flex items-start">
          <div class="bg-white border border-[#d2d2d7]/30 shadow-sm px-4 py-3 rounded-2xl">
            <div class="flex gap-1.5 items-center h-5">
              <span class="w-1.5 h-1.5 bg-[#d2d2d7] rounded-full animate-bounce" style="animation-delay: 0ms"></span>
              <span class="w-1.5 h-1.5 bg-[#d2d2d7] rounded-full animate-bounce" style="animation-delay: 150ms"></span>
              <span class="w-1.5 h-1.5 bg-[#d2d2d7] rounded-full animate-bounce" style="animation-delay: 300ms"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="relative flex items-center gap-3">
        <div class="relative flex-1">
          <input 
            v-model="question" 
            @keyup.enter="handleSend"
            placeholder="询问您的知识库..."
            class="w-full bg-white border border-[#d2d2d7]/50 rounded-2xl px-5 py-4 text-[15px] outline-none focus:border-[#0071e3]/50 transition-all shadow-sm pr-12"
            :disabled="isLoading"
          />
          <button 
            @click="handleSend"
            class="absolute right-3 top-1/2 -translate-y-1/2 w-8 h-8 rounded-xl flex items-center justify-center transition-all"
            :class="question.trim() ? 'bg-[#0071e3] text-white' : 'bg-[#f5f5f7] text-[#d2d2d7]'"
            :disabled="!question.trim() || isLoading"
          >
            <Send class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { Library, MessageSquare, Send } from 'lucide-vue-next'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const question = ref('')
const isLoading = ref(false)
const chatHistory = ref<Message[]>([])
const chatContainer = ref<HTMLElement | null>(null)

const renderMarkdown = (content: string) => {
  return marked(content)
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const clearChat = () => {
  chatHistory.value = []
}

const handleSend = async () => {
  if (!question.value.trim() || isLoading.value) return

  const userMsg = question.value.trim()
  chatHistory.value.push({ role: 'user', content: userMsg })
  question.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    const response = await fetch('http://localhost:8000/note/ai/rag', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: userMsg })
    })
    
    if (!response.ok) throw new Error('请求失败')
    
    const data = await response.json()
    chatHistory.value.push({ role: 'assistant', content: data.answer })
  } catch (err) {
    ElMessage.error('问答请求失败，请检查后端连接')
    chatHistory.value.push({ role: 'assistant', content: '抱歉，我现在无法处理您的问题。请稍后再试。' })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.prose :deep(p) { margin-bottom: 0.5em; }
.prose :deep(p:last-child) { margin-bottom: 0; }
</style>
