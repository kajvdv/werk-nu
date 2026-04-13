<script setup lang="ts">
import Badge from '@/components/ui/Badge.vue';
import Button from '@/components/ui/Button.vue';
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const authStore  = useAuthStore()
const entityType = computed(() => {
  const entityType = authStore.user.entity_type
  if (entityType === "organization") {
    return "Werkgever"
  } else if (entityType === "user") {
    return "Werkzoekende"
  }
})
</script>

<template>
  <div class="flex items-center justify-between bg-ink px-6 py-4">
    <div class="text-5xl font-title tracking-title text-paper">werk<span class="text-accent">.</span>nu</div>
    <div class="flex gap-3">
      <Badge color="ghost">Ingelogd als: {{ entityType }}</Badge>
      <Button v-if="entityType == 'Werkgever'" type="ghost">Mijn vacatures</Button>
      <Button v-else type="ghost">Mijn sollicitaties</Button>
      <Button v-if="entityType == 'Werkgever'" type="primary" @click="() => router.push('/vacancies/post')">+ Nieuwe vacature</Button>
    </div>
  </div>
</template>
