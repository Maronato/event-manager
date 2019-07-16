<template>
    <base-layout>
        <nuxt />
    </base-layout>
</template>

<script>
    import baseLayout from './base'
    export default {
        components: { baseLayout },
        options: {
            auth: false
        },
        data() {
            return {
                page_title: 'Login'
            }
        },
    }
</script>
