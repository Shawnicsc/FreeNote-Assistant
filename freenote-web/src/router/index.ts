import { createRouter, createWebHistory } from 'vue-router'
import EditorPage from '@/pages/EditorPage.vue'
import KnowledgePage from '@/pages/KnowledgePage.vue'
import SettingsPage from '@/pages/SettingsPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/editor',
    },
    {
      path: '/editor',
      component: EditorPage,
    },
    {
      path: '/knowledge',
      component: KnowledgePage,
    },
    {
      path: '/settings',
      component: SettingsPage,
    },
  ],
})

export default router
