<template>
  <div class="h-full flex flex-col bg-[#f5f5f7]">
    <!-- Minimalist Toolbar -->
    <div class="h-14 px-6 flex items-center justify-between border-b border-[#d2d2d7]/30 bg-white/50 backdrop-blur-sm sticky top-0 z-10">
      <div class="flex items-center gap-3">
        <FileText class="w-4 h-4 text-[#86868b]" />
        <span class="text-[13px] font-medium text-[#1d1d1f] truncate max-w-[200px]">
          {{ fileName || '未命名文档' }}
        </span>
        <span v-if="documentStore.isDirty" class="w-1.5 h-1.5 rounded-full bg-orange-400"></span>
      </div>

      <div class="flex items-center gap-2">
        <!-- View Toggle -->
        <div class="flex items-center bg-[#f5f5f7] rounded-lg p-0.5 mr-4">
          <button 
            @click="viewMode = 'edit'"
            :class="viewMode === 'edit' ? 'bg-white shadow-sm text-[#1d1d1f]' : 'text-[#86868b]'"
            class="px-3 py-1 text-[12px] font-medium rounded-md transition-all"
          >
            编辑
          </button>
          <button 
            @click="viewMode = 'preview'"
            :class="viewMode === 'preview' ? 'bg-white shadow-sm text-[#1d1d1f]' : 'text-[#86868b]'"
            class="px-3 py-1 text-[12px] font-medium rounded-md transition-all"
          >
            预览
          </button>
        </div>

        <div class="flex items-center bg-[#f5f5f7] rounded-lg p-0.5 mr-2">
          <button 
            @click="handleSummary" 
            :disabled="isAIProcessing || !documentStore.content"
            class="px-3 py-1 text-[12px] font-medium rounded-md hover:bg-white hover:shadow-sm transition-all text-[#1d1d1f] disabled:opacity-50"
          >
            {{ isAIProcessing ? '分析中...' : '总结' }}
          </button>
          <button 
            @click="handleRewrite" 
            :disabled="isAIProcessing || !documentStore.content"
            class="px-3 py-1 text-[12px] font-medium rounded-md hover:bg-white hover:shadow-sm transition-all text-[#1d1d1f] disabled:opacity-50"
          >
            润色
          </button>
          <button class="px-3 py-1 text-[12px] font-medium rounded-md hover:bg-white hover:shadow-sm transition-all text-[#1d1d1f]">UML</button>
        </div>

        <button @click="openFile" class="apple-button-secondary !py-1.5 !px-3 text-[13px] gap-1.5">
          <Upload class="w-3.5 h-3.5" />
          打开
        </button>
        <button 
          @click="saveFile" 
          :disabled="!documentStore.isDirty"
          class="apple-button-primary !py-1.5 !px-3 text-[13px] gap-1.5"
        >
          <Save class="w-3.5 h-3.5" />
          保存
        </button>
      </div>
    </div>

    <!-- Main Editor Area -->
    <div class="flex-1 overflow-auto py-8 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto apple-card min-h-full p-8 md:p-12 lg:p-16">
        <MarkdownEditor v-if="viewMode === 'edit'" v-model="documentStore.content" />
        <div v-else class="prose prose-slate max-w-none markdown-preview" v-html="renderedMarkdown"></div>
      </div>
    </div>

    <!-- AI Summary Dialog -->
    <el-dialog
      v-model="summaryDialogVisible"
      title="文档智能总结"
      width="600px"
      custom-class="apple-dialog"
    >
      <div v-if="summaryData" class="space-y-6">
        <div>
          <h3 class="text-lg font-bold text-[#1d1d1f] mb-2">{{ summaryData.title }}</h3>
          <p class="text-[15px] leading-relaxed text-[#424245]">{{ summaryData.summary }}</p>
        </div>
        
        <div v-if="summaryData.key_points && summaryData.key_points.length">
          <h4 class="text-sm font-semibold text-[#86868b] uppercase tracking-wider mb-3">关键要点</h4>
          <ul class="space-y-2">
            <li v-for="(point, index) in summaryData.key_points" :key="index" class="flex items-start gap-2 text-[14px]">
              <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-[#0071e3] flex-shrink-0"></span>
              {{ point }}
            </li>
          </ul>
        </div>

        <div v-if="summaryData.structure && summaryData.structure.length">
          <h4 class="text-sm font-semibold text-[#86868b] uppercase tracking-wider mb-3">章节结构</h4>
          <div class="space-y-4">
            <div v-for="(item, index) in summaryData.structure" :key="index" class="bg-[#f5f5f7] p-3 rounded-xl">
              <div class="font-medium text-[#1d1d1f] mb-1">{{ item.section }}</div>
              <div class="text-sm text-[#86868b]">{{ item.description }}</div>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <button @click="summaryDialogVisible = false" class="apple-button-primary px-6">关闭</button>
      </template>
    </el-dialog>

    <!-- AI Rewrite Dialog -->
    <el-dialog
      v-model="rewriteDialogVisible"
      title="文档智能润色"
      width="800px"
      custom-class="apple-dialog"
    >
      <div v-if="rewriteData" class="grid grid-cols-2 gap-6 h-[500px]">
        <div class="flex flex-col">
          <h4 class="text-xs font-semibold text-[#86868b] uppercase mb-2">修改建议</h4>
          <div class="flex-1 overflow-auto bg-[#f5f5f7] p-4 rounded-xl">
            <ul class="space-y-3">
              <li v-for="(change, index) in rewriteData.changes_summary" :key="index" class="text-[13px] flex items-start gap-2">
                <span class="mt-1 text-[#0071e3]">✓</span>
                {{ change }}
              </li>
            </ul>
          </div>
        </div>
        <div class="flex flex-col">
          <h4 class="text-xs font-semibold text-[#86868b] uppercase mb-2">润色后内容</h4>
          <div class="flex-1 overflow-auto border border-[#d2d2d7]/30 p-4 rounded-xl text-[14px] leading-relaxed whitespace-pre-wrap">
            {{ rewriteData.rewritten_content }}
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <button @click="rewriteDialogVisible = false" class="apple-button-secondary px-6">取消</button>
          <button @click="applyRewrite" class="apple-button-primary px-6">采用修改</button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import MarkdownEditor from '@/editor/MarkdownEditor.vue'
import { documentStore, replaceDocumentContent } from '@/document/document.store'
import { watch } from 'vue'
import { ElMessage } from 'element-plus'
import { FileText, Upload, Save } from 'lucide-vue-next'
import { marked } from 'marked'

const fileName = ref('')
const viewMode = ref<'edit' | 'preview'>('edit')
const isAIProcessing = ref(false)
let currentFileHandle: any = null

// AI Dialog States
const summaryDialogVisible = ref(false)
const summaryData = ref<any>(null)
const rewriteDialogVisible = ref(false)
const rewriteData = ref<any>(null)

const renderedMarkdown = computed(() => {
  return marked(documentStore.content || '')
})

watch(
  () => documentStore.content,
  () => {
    documentStore.isDirty = true
  }
)

async function handleSummary() {
  if (!documentStore.content) return
  isAIProcessing.value = true
  try {
    const response = await fetch('http://localhost:8000/summary', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: documentStore.content })
    })
    const data = await response.json()
    summaryData.value = typeof data === 'string' ? JSON.parse(data) : data
    summaryDialogVisible.value = true
  } catch (err) {
    ElMessage.error('总结生成失败，请检查后端连接')
    console.error(err)
  } finally {
    isAIProcessing.value = false
  }
}

async function handleRewrite() {
  if (!documentStore.content) return
  isAIProcessing.value = true
  try {
    const response = await fetch('http://localhost:8000/rewrite', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: documentStore.content })
    })
    const data = await response.json()
    rewriteData.value = typeof data === 'string' ? JSON.parse(data) : data
    rewriteDialogVisible.value = true
  } catch (err) {
    ElMessage.error('润色生成失败，请检查后端连接')
    console.error(err)
  } finally {
    isAIProcessing.value = false
  }
}

function applyRewrite() {
  if (rewriteData.value?.rewritten_content) {
    replaceDocumentContent(rewriteData.value.rewritten_content)
    rewriteDialogVisible.value = false
    ElMessage.success('已应用润色内容')
  }
}

async function openFile() {
  try {
    const [fileHandle] = await (window as any).showOpenFilePicker({
      types: [
        {
          description: 'Markdown Files',
          accept: {
            'text/markdown': ['.md'],
          },
        },
      ],
      multiple: false,
    })

    const file = await fileHandle.getFile()
    const content = await file.text()
    currentFileHandle = fileHandle
    fileName.value = file.name

    replaceDocumentContent(content)
    ElMessage.success('文件已加载')
  } catch (err: any) {
    if (err?.name === 'AbortError') {
      ElMessage.info('已取消打开文件')
      return
    }
    ElMessage.error('文件打开失败')
    console.error(err)
  }
}

async function saveFile() {
  try {
    if (!currentFileHandle) {
      currentFileHandle = await (window as any).showSaveFilePicker({
        suggestedName: 'note.md',
        types: [
          {
            description: 'Markdown Files',
            accept: {
              'text/markdown': ['.md'],
            },
          },
        ],
      })
      const file = await currentFileHandle.getFile()
      fileName.value = file.name
    }

    const writable = await currentFileHandle.createWritable()
    await writable.write(documentStore.content)
    await writable.close()

    documentStore.isDirty = false
    ElMessage.success('保存成功')
  } catch (err: any) {
    if (err?.name === 'AbortError') {
      ElMessage.info('已取消保存')
      return
    }
    ElMessage.error('保存失败')
    console.error(err)
  }
}
</script>

<style scoped>
@reference "../assets/global.css";

.markdown-preview :deep(h1) { @apply text-4xl font-bold mb-6 mt-8; }
.markdown-preview :deep(h2) { @apply text-3xl font-semibold mb-4 mt-6; }
.markdown-preview :deep(h3) { @apply text-2xl font-semibold mb-3 mt-5; }
.markdown-preview :deep(p) { @apply text-[16px] leading-relaxed mb-4 text-[#1d1d1f]; }
.markdown-preview :deep(ul) { @apply list-disc pl-6 mb-4; }
.markdown-preview :deep(ol) { @apply list-decimal pl-6 mb-4; }
.markdown-preview :deep(code) { @apply bg-[#f5f5f7] px-1.5 py-0.5 rounded text-[#e03131] font-mono text-sm; }
.markdown-preview :deep(pre) { @apply bg-[#f5f5f7] p-4 rounded-xl overflow-auto mb-4 border border-[#d2d2d7]/30; }
.markdown-preview :deep(blockquote) { @apply border-l-4 border-[#d2d2d7] pl-4 italic text-[#86868b] mb-4; }
</style>
