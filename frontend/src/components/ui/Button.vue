<script setup lang="ts">
import { computed } from 'vue';

const {type = "primary", small = false} = defineProps<{
    type?: "primary" | "ghost" | "outline" | "red"
    small?: boolean
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
        outline: [
            "bg-transparent",
            "text-ink",
            "border",
            "border-border"
        ].join(" "),
        red: [
            "bg-red-100",
            "text-red-800",
            "border-0",
        ].join(" "),
        ghost: [
            "hover:opacity-85 text-paper",
            "border border-white/20",
        ].join(" ")
    }

    return `${base} ${variants[type] ?? variants.primary} ${small ? "text-sm" : ""}`
})

</script>

<template>
    <button v-bind="$attrs" :class="classNames">
        <slot/>
    </button>
</template>