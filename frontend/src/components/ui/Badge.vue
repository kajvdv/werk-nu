<script setup lang="ts">
import { computed } from 'vue';

const { color } = defineProps<{color: "red" | "green" | "yellow" | "ghost"}>()

const classNames = computed(() => {
    const base = "text-xs text-muted bg px-3 py-1 rounded-full self-center"
// green: inline-block py-1 px-3 rounded-2xl text-xs font-medium
    const variants = {
        red: "",
        green: "text-green-800 bg-green-100 font-medium",
        yellow: "text-orange-800 bg-orange-50 font-medium",
        ghost: "bg-white/8"
    }

    return `${base} ${variants[color]}`
})
</script>

<template>
    <span :class="classNames">
        <slot/>
    </span>
</template>