<template>
    <div>
        <div class="description">
            <b>Atenção!</b>
            Você tem até {{ reg_date }} pra {{ actionWord }} sua aplicação.
        </div>
        <v-btn
            router
            nuxt
            tile
            to="/application"
            color="primary">{{ actionWord }} sua aplicação</v-btn>
    </div>
</template>
<script>
    export default {
        computed: {
            reg_date() {
                return this.$moment(this.$store.state.settings.settings.registration_close_seconds).calendar()
            },
            actionWord() {
                if (this.$auth.user.state === 'incomplete') {
                    return 'completar'
                }
                return 'modificar'
            }
        }
    }
</script>
