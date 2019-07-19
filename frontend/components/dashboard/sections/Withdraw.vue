<template>
    <div>
        <v-divider />
        <br />
        <div class="header divided big-title">Não poderá participar?</div>
        <div class="description">
            <b>Nos avise!</b> Assim poderemos cancelar sua inscrição e liberar a vaga para outra pessoa :)
            <br />
            Você ainda pode mudar de ideia até {{ conf_close }}.
            <template
                v-if="this.$store.state.settings.settings.require_payment"
            >
                <br />
                <b>Nós vamos extornar seu ticket imediatamente caso você desista do evento.</b>
            </template>
        </div>
        <br />
        <v-btn
            color="primary"
            :loading="loading"
            :disabled="loading"
            @click="withdraw()"
            v-text="`Desculpe, não vou conseguir`"
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
            withdraw() {
                this.loading = true
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/hackers/me/withdraw/"
                    })
                    .then(data => {
                        this.$toast("Que pena :(", data.message, "info")
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
