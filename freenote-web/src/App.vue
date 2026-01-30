<template>
  <div class="min-h-screen flex flex-col">
    <!-- Apple Style Glass Header -->
    <header class="glass-header h-12 flex items-center justify-between px-6">
      <div class="flex items-center gap-8">
        <div class="flex items-center gap-2 cursor-pointer group" @click="router.push('/editor')">
          <div class="w-6 h-6 bg-black rounded-md flex items-center justify-center group-hover:scale-105 transition-transform">
            <span class="text-white text-[10px] font-bold">FN</span>
          </div>
          <span class="text-[15px] font-semibold tracking-tight">FreeNote</span>
        </div>
        
        <nav class="hidden md:flex items-center gap-6">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            class="text-[13px] font-medium transition-colors hover:text-[#0071e3]"
            :class="[route.path.startsWith(item.path) ? 'text-[#1d1d1f]' : 'text-[#86868b]']"
          >
            {{ item.name }}
          </router-link>
        </nav>
      </div>

      <div class="flex items-center gap-4">
        <!-- Optional: User Profile or Quick Actions -->
      </div>
    </header>

    <main class="flex-1 overflow-auto">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const navItems = [
  { name: '编辑器', path: '/editor' },
  { name: '知识库', path: '/knowledge' },
  { name: '设置', path: '/settings' },
]
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
