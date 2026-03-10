import { createRouter, createWebHistory } from 'vue-router'
import DocumentsView from '@/views/DocumentsView.vue'
import DocumentFormView from '@/views/DocumentFormView.vue'
import DocumentDetailsView from '@/views/DocumentDetailsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'documents',
      component: DocumentsView
    },
    {
      path: '/create',
      name: 'create',
      component: DocumentFormView
    },
    {
      path: '/view/:id',
      name: 'view',
      component: DocumentDetailsView
    },
    {
      path: '/edit/:id',
      name: 'edit',
      component: DocumentFormView
    }
  ]
})

export default router