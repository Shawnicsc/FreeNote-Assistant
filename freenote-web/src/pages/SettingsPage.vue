<template>
  <div class="h-full bg-[#f5f5f7] py-12 px-6">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-4xl font-bold tracking-tight text-[#1d1d1f] mb-8">设置</h1>
      
      <div class="space-y-6">
        <section class="apple-card p-6">
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <Cpu class="w-5 h-5 text-[#0071e3]" />
            AI 模型配置
          </h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between py-2 border-b border-[#d2d2d7]/30">
              <div>
                <p class="font-medium">当前模型</p>
                <p class="text-sm text-[#86868b]">选择用于智能分析的 AI 模型</p>
              </div>
              <select class="bg-[#f5f5f7] rounded-lg px-3 py-1.5 text-sm outline-none border-none">
                <option>GPT-4o</option>
                <option>Claude 3.5 Sonnet</option>
              </select>
            </div>
          </div>
        </section>

        <section class="apple-card p-6">
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <Palette class="w-5 h-5 text-[#0071e3]" />
            外观设置
          </h3>
          <div class="flex items-center justify-between py-2">
            <div>
              <p class="font-medium">深色模式</p>
              <p class="text-sm text-[#86868b]">自动切换日间与夜间模式</p>
            </div>
            <div class="w-12 h-6 bg-[#d2d2d7] rounded-full relative cursor-pointer">
              <div class="absolute left-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm transition-all"></div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Cpu, Palette } from 'lucide-vue-next'
</script>
