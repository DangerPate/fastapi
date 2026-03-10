<template>
  <div class="container">
    <h2 text-aligh="center">{{ isEdit ? 'Редактировать документ' : 'Создать новый документ' }}</h2>
    <div class="document-form">
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>Номер документа</label>
          <input class="input-form-group" v-model="form.document_number" required minlength="3" maxlength="50" />
        </div>
        <div class="form-group">
          <label>Название</label>
          <input class="input-form-group" v-model="form.document_name" required minlength="3" maxlength="200" />
        </div>
        <div class="form-group">
          <label>Тип</label>
          <select class="input-form-group" v-model="form.document_type" required>
            <option value="licence">Лицензия</option>
            <option value="sro certificate">Сертификат СРО</option>
            <option value="accreditation">Аккредитация</option>
            <option value="iso_certificate">Сертификат ISO</option>
            <option value="fstec_license">Лицензия ФСТЭК</option>
          </select>
        </div>
        <div class="form-group">
          <label>Орган, выдавший документ</label>
          <input class="input-form-group" v-model="form.issuer" required minlength="3" maxlength="200" />
        </div>
        <div class="form-group">
          <label>Дата выдачи</label>
          <input type="date" v-model="form.issue_date" required />
        </div>
        <div class="form-group">
          <label>Дата начала действия</label>
          <input type="date" v-model="form.valid_from" required />
        </div>
        <div class="form-group">
          <label>Дата окончания действия</label>
          <input type="date" v-model="form.valid_until" required :disabled="form.is_indefinite" />
        </div>
        <div class="form-group">
          <label class="custom-checkbox-wrapper">
            <span class="custom-checkbox-label">Бессрочно</span>
            <input type="checkbox" v-model="form.is_indefinite" class="custom-checkbox-input" />
            <span class="custom-checkbox-box"></span>
          </label>
        </div>
        <div class="form-group">
          <label>Статус</label>
          <select v-model="form.status" required>
            <option value="active">Активный</option>
            <option value="expiring_soon">Скоро истекает</option>
            <option value="expired">Просрочен</option>
            <option value="suspended">Приостановлен</option>
            <option value="revoked">Аннулирован</option>
            <option value="archived">Архивный</option>
          </select>
        </div>
        <div class="form-group">
          <label>Владелец</label>
          <input class="input-form-group" v-model="form.holder_name" required minlength="3" maxlength="200" />
        </div>
        <div class="form-group">
          <label>Описание</label>
          <textarea v-model="form.description" maxlength="200"></textarea>
        </div>

        <button type="submit" class="btn btn-success">{{ isEdit ? 'Сохранить' : 'Создать' }}</button>
        <router-link to="/" class="btn btn-secondary">Отмена</router-link>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const isEdit = ref(false)
const toast = useToast()

const form = ref({
  document_number: '',
  document_name: '',
  document_type: 'licence',
  issuer: '',
  issue_date: '',
  valid_from: '',
  valid_until: '',
  status: 'active',
  holder_name: '',
  is_indefinite: false,
  description: ''
})

onMounted(async () => {
  if (route.params.id) {
    isEdit.value = true
    try {
      const response = await api.getDocument(route.params.id)
      const doc = response.data
      form.value = {
        ...doc,
        issue_date: doc.issue_date ? doc.issue_date.slice(0, 10) : '',
        valid_from: doc.valid_from ? doc.valid_from.slice(0, 10) : '',
        valid_until: doc.valid_until ? doc.valid_until.slice(0, 10) : ''
      }
    } catch (error) {
      console.error('Ошибка загрузки документа:', error)
      toast.error('Не удалось загрузить данные документа')
      router.push('/')
    }
  }
})

const submitForm = async () => {
  try {
    if (isEdit.value) {
      await api.updateDocument(route.params.id, form.value)
      toast.success('Документ обновлён')
    } else {
      await api.createDocument(form.value)
      toast.success('Документ создан')
    }
    router.push('/')
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    if (error.response && error.response.status === 400) {
      toast.error(error.response.data.detail || 'Ошибка валидации')
    } else {
      toast.error('Не удалось сохранить документ')
    }
  }
}
</script>

<style scoped>
</style>