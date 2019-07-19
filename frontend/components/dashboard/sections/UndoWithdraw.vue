<template>
    <div>
        <v-divider />
        <br />
        <div class="header divided big-title">Mudar de ideia</div>
        <div class="description">
            <b>Você ainda tem até {{ conf_close }} para reativar sua aplicação!</b>
        </div>
        <br />
        <v-btn
            color="primary"
            :loading="loading"
            :disabled="loading"
            tile
            @click="undo_withdraw()"
            v-text="`Mudei de ideia!`"
        />
        <br />
    </div>
</template>

<script>
    export default {
        data() {
            return {
                loading: false
            }
        },
        computed: {
            conf_close() {
                return this.$moment(
                    this.$store.state.settings.settings.confirmation_seconds
                ).calendar()
            }
        },
        methods: {
            undo_withdraw() {
                self.loading = true
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/hackers/me/undo_withdraw/"
                    })
                    .then(data => {
                        this.$toast("Ótimo!", data.message, "success")
                        this.loading = false
                    })
                    .catch(error => {
                        this.$toast("Opa!", "Algo de errado aconteceu :(", "error")
                        this.loading = false
                        return Promise.reject(error)
                    })
            }
        }
    }
</script>
