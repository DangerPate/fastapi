<template>
  <div class="container">
    <h1>Реестр лицензий и сертификатов</h1>
    <!-- Фильтр по статусу и кнопка создания -->
    <div class="filters">
      <select v-model="statusFilter" @change="loadDocuments">
        <option value="">Все статусы</option>
        <option value="active">Активные</option>
        <option value="expiring_soon">Истекают скоро</option>
        <option value="expired">Просроченные</option>
        <option value="suspended">Приостановленные</option>
        <option value="revoked">Аннулированные</option>
        <option value="archived">Архивные</option>
      </select>
      <div class="search-section">
        <button @click="searchDocument" class="btn btn-primary">Найти</button>
        <input 
          type="number" 
          v-model.number="searchId" 
          placeholder="Введите ID документа" 
          min="1"
          @keyup.enter="searchDocument"
        />
        <router-link to="/create" class="btn btn-primary">Создать документ</router-link>
      </div>
      
    </div>

    <!-- Таблица документов -->
    <table v-if="documents.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Номер</th>
          <th>Название</th>
          <th>Тип</th>
          <th>Владелец</th>
          <th>Статус</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="doc in documents" :key="doc.id">
          <td>{{ doc.id }}</td>
          <td>{{ doc.document_number }}</td>
          <td>{{ doc.document_name }}</td>
          <td>{{ doc.document_type }}</td>
          <td>{{ doc.holder_name }}</td>
          <td>
            <span :class="'status ' + doc.status">{{ statusTranslations[doc.status] || doc.status }}</span>
          </td>
          <td>
            <router-link :to="`/view/${doc.id}`" class="btn-view">Просмотреть</router-link>
            <router-link :to="`/edit/${doc.id}`" class="btn-edit">Редактировать</router-link>
            <button @click="deleteDocument(doc.id)" class="btn-delete">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Документов нет.</p>

    <!-- Пагинация (упрощённая) -->
    <div class="pagination">
      <button @click="prevPage" :disabled="skip === 0">Назад</button>
      <span>Страница {{ currentPage + 1 }}</span>
      <button @click="nextPage" :disabled="documents.length < limit">Вперёд</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { statusTranslations } from '@/constants/statuses'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'


const documents = ref([])
const statusFilter = ref('')
const skip = ref(0)
const limit = ref(10)
const currentPage = ref(0)
const toast = useToast()
const router = useRouter()
const searchId = ref(null) 

const loadDocuments = async () => {
  try {
    const response = await api.getDocuments(skip.value, limit.value, statusFilter.value || null)
    documents.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки:', error)
    toast.error('Не удалось загрузить документ')
  }
}

const deleteDocument = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить документ?')) return
  try {
    await api.deleteDocument(id)
    await loadDocuments() // перезагружаем список
  } catch (error) {
    console.error('Ошибка удаления:', error)
    toast.error('Не удалось удалить документ')
  }
}

const prevPage = () => {
  if (skip.value >= limit.value) {
    skip.value -= limit.value
    currentPage.value--
    loadDocuments()
  }
}

const nextPage = () => {
  skip.value += limit.value
  currentPage.value++
  loadDocuments()
}

const searchDocument = async () => {
  if (!searchId.value || searchId.value <= 0) {
    toast.warning('Введите корректный ID (положительное число)')
    return
  }
  try {
    await api.getDocument(searchId.value)
    router.push(`/view/${searchId.value}`)
  } catch (error) {
    if (error.response && error.response.status === 404) {
      toast.error(`Документ с ID ${searchId.value} не найден`)
    } else {
      toast.error('Ошибка при поиске документа')
    }
  }
}

onMounted(loadDocuments)
</script>

<style scoped>
</style>