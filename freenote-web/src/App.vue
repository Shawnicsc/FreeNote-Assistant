<template>
  <el-container class="app-shell">
    <el-header height="48px" class="app-header">
      <el-menu
        mode="horizontal"
        :default-active="activePath"
        router
      >
        <el-menu-item index="/editor">编辑</el-menu-item>
        <el-menu-item index="/knowledge">知识库</el-menu-item>
        <el-menu-item index="/settings">设置</el-menu-item>
      </el-menu>
    </el-header>

    <el-main class="app-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const activePath = route.path
</script>

<style scoped>
.app-header {
  height: 44px;
  background: #ffffff;
  border-bottom: 1px solid #e6e8eb;
}

.app-main {
  padding: 16px;
}
.el-menu--horizontal {
  border-bottom: none;
}

.el-menu-item {
  font-size: 14px;
  color: #555;
}

.el-menu-item.is-active {
  font-weight: 500;
  color: #111;
}

</style>
