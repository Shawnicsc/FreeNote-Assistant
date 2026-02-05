<template>
  <div class="h-full bg-[#f5f5f7] py-12 px-6 overflow-y-auto">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-4xl font-bold tracking-tight text-[#1d1d1f] mb-8">设置</h1>
      
      <div class="space-y-6">
        <!-- AI API Configuration -->
        <section class="apple-card p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold flex items-center gap-2">
              <Cpu class="w-5 h-5 text-[#0071e3]" />
              AI API 配置
            </h3>
            <button 
              @click="saveConfig" 
              :disabled="isSaving"
              class="apple-button-primary !py-1.5 !px-4 text-[13px]"
            >
              {{ isSaving ? '保存中...' : '保存配置' }}
            </button>
          </div>

          <div class="space-y-6">
            <div class="space-y-2">
              <label class="text-[13px] font-medium text-[#86868b] uppercase tracking-wider">API Key</label>
              <input 
                v-model="config.api_key" 
                type="password"
                placeholder="sk-..."
                class="w-full bg-[#f5f5f7] rounded-xl px-4 py-3 text-[15px] outline-none border border-transparent focus:border-[#0071e3]/30 transition-all"
              />
            </div>

            <div class="space-y-2">
              <label class="text-[13px] font-medium text-[#86868b] uppercase tracking-wider">Base URL</label>
              <input 
                v-model="config.base_url" 
                placeholder="https://api.openai.com/v1"
                class="w-full bg-[#f5f5f7] rounded-xl px-4 py-3 text-[15px] outline-none border border-transparent focus:border-[#0071e3]/30 transition-all"
              />
            </div>

            <div class="space-y-2">
              <label class="text-[13px] font-medium text-[#86868b] uppercase tracking-wider">Model ID</label>
              <input 
                v-model="config.model_id" 
                placeholder="gpt-4o"
                class="w-full bg-[#f5f5f7] rounded-xl px-4 py-3 text-[15px] outline-none border border-transparent focus:border-[#0071e3]/30 transition-all"
              />
            </div>
          </div>
        </section>

        <!-- Appearance -->
        <section class="apple-card p-6 opacity-50 cursor-not-allowed">
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <Palette class="w-5 h-5 text-[#0071e3]" />
            外观设置 (即将推出)
          </h3>
          <div class="flex items-center justify-between py-2">
            <div>
              <p class="font-medium text-[#1d1d1f]">深色模式</p>
              <p class="text-sm text-[#86868b]">自动切换日间与夜间模式</p>
            </div>
            <div class="w-12 h-6 bg-[#d2d2d7] rounded-full relative">
              <div class="absolute left-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm"></div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Cpu, Palette } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

const isSaving = ref(false)
const config = ref({
  api_key: '',
  base_url: '',
  model_id: ''
})

const fetchConfig = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/ai/config')
    if (response.ok) {
      const data = await response.json()
      // 注意：api_key 返回的是脱敏后的，这里仅展示占位
      config.value.base_url = data.base_url || ''
      config.value.model_id = data.model_id || ''
    }
  } catch (err) {
    console.error('获取配置失败:', err)
  }
}

const saveConfig = async () => {
  isSaving.value = true
  try {
    const response = await fetch('http://localhost:8000/api/v1/ai/config/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config.value)
    })
    
    if (!response.ok) throw new Error('保存失败')
    
    ElMessage.success('配置已更新')
  } catch (err) {
    ElMessage.error('配置保存失败')
  } finally {
    isSaving.value = false
  }
}

onMounted(fetchConfig)
</script>
