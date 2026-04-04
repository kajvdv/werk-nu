<script setup lang="ts">
import Badge from '@/components/ui/Badge.vue';
import Button from '@/components/ui/Button.vue';
</script>

<template>
  <div class="flex items-center justify-between bg-ink px-6 py-4">
    <div class="text-5xl font-title tracking-title text-paper">werk<span class="text-accent">.</span>nu</div>
    <div class="flex gap-3">
      <Badge color="ghost">Ingelogd als: Werkzoekende</Badge>
      <Button type="ghost">Mijn sollicitaties</Button>
    </div>
  </div>
</template>
