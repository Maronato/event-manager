<template>
    <base-layout>
        <nuxt />
    </base-layout>
</template>

<script>
    import baseLayout from './base'
    export default {
        components: { baseLayout },
        auth: false,
        data() {
            return {
                pageTitle: 'Login'
            }
        },
        head() {
            return {
                title: this.pageTitle
            }
        },
    }
</script>
