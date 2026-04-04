<script setup lang="ts">
import { computed } from 'vue';

const {type = "primary"} = defineProps<{
    type: "primary" | "ghost"
}>()

const classNames = computed(() => {
    const base = [
        "px-4 py-1",
        "rounded-md",
        "cursor-pointer",
        "font-dm",
        "transition-opacity duration-200",
    ].join(" ")
    
    const variants = {
        primary: [
            "text-white",
            "bg-accent"
        ].join(" "),
        ghost: [
            "hover:opacity-85 text-paper",
            "border border-white/20",
        ].join(" ")
    }

    return `${base} ${variants[type] ?? variants.primary}`
})

</script>

<template>
    <button :class="classNames">
        <slot/>
    </button>
</template>