<template>
  <div class="container">
    <h2>Просмотр документа</h2>
    <div v-if="document" class="document-details">
      <div class="detail-row">
        <strong>ID:</strong> {{ document.id }}
      </div>
      <div class="detail-row">
        <strong>Номер документа:</strong> {{ document.document_number }}
      </div>
      <div class="detail-row">
        <strong>Название:</strong> {{ document.document_name }}
      </div>
      <div class="detail-row">
        <strong>Тип:</strong> {{ document.document_type }}
      </div>
      <div class="detail-row">
        <strong>Орган, выдавший документ:</strong> {{ document.issuer }}
      </div>
      <div class="detail-row">
        <strong>Дата выдачи:</strong> {{ formatDate(document.issue_date) }}
      </div>
      <div class="detail-row">
        <strong>Дата начала действия:</strong> {{ formatDate(document.valid_from) }}
      </div>
      <div class="detail-row">
        <strong>Дата окончания действия:</strong> {{ formatDate(document.valid_until) }}
      </div>
      <div class="detail-row">
        <strong>Статус:</strong> 
        <span :class="'detail-row-status' + document.status">{{ statusTranslations[document.status] || document.status }}</span>
      </div>
      <div class="detail-row">
        <strong>Владелец:</strong> {{ document.holder_name }}
      </div>
      <div class="detail-row">
        <strong>Бессрочный:</strong> {{ document.is_indefinite ? 'Да' : 'Нет' }}
      </div>
      <div class="detail-row" v-if="document.description">
        <strong>Описание:</strong> {{ document.description }}
      </div>
      <div class="actions">
        <router-link to="/" class="btn btn-secondary">Назад к списку</router-link>
        <router-link :to="`/edit/${document.id}`" class="btn btn-primary">Редактировать</router-link>
      </div>
    </div>
    <div v-else-if="loading">Загрузка...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import type { Document } from '@/types/document';
import { statusTranslations } from '@/constants/statuses';
import { useToast } from 'vue-toastification'

const route = useRoute();
const router = useRouter();
const document = ref<Document | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const toast = useToast()

const formatDate = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU');
};

onMounted(async () => {
  const id = Number(route.params.id);
  if (isNaN(id)) {
    error.value = 'Неверный идентификатор документа';
    loading.value = false;
    return;
  }

  try {
    const response = await api.getDocument(id);
    document.value = response.data;
  } catch (err) {
    console.error('Ошибка загрузки документа:', err);
    error.value = 'Не удалось загрузить документ';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
</style>