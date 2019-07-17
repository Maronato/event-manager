<template>
    <div>
        <v-divider />
        <br />
        <div class="header divided big-title">Confirmar presença</div>
        <div class="description">
            <b>Atenção!</b>
            Você ainda precisa confirmar sua presença até {{ conf_close }}
            <br />
            <br />
            <b>Não confirmar sua presença até esse dia significará a perda de seu lugar no evento!</b>
        </div>
        <v-btn
            color="blue"
            class="white--text"
            tile
            :loading="loading"
            :disabled="loading"
            @click="confirm()"
        >Confirmar presença</v-btn>
        <br />
        <br />
        <div class="description">
            Não vai poder participar? Nos avise!
            <template
                v-if="$store.state.settings.settings.require_payment"
            >
                <br />
                <b>Nós vamos extornar seu ticket imediatamente caso você desista do evento.</b>
            </template>
        </div>
        <v-btn
            color="red"
            class="white--text"
            tile
            :loading="loading"
            :disabled="loading"
            @click="withdraw()"
        >Não posso participar</v-btn>
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
            reg_close() {
                return this.$moment(
                    this.$store.state.settings.settings.registration_close_seconds
                ).calendar()
            },
            conf_close() {
                return this.$moment(
                    this.$store.state.settings.settings.confirmation_seconds
                ).calendar()
            }
        },
        methods: {
            confirm() {
                this.loading = true
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/hackers/me/confirm/"
                    })
                    .then(data => {
                        this.$toast("Sucesso!", data.message, "success")
                        this.loading = false
                    })
                    .catch(error => {
                        this.$toast("Opa!", "Algo de errado aconteceu :(", "error")
                        this.loading = false
                        return Promise.reject(error)
                    })
            },
            withdraw() {
                this.loading = true
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/hackers/me/withdraw/"
                    })
                    .then(data => {
                        this.$toast("Pronto!", data.message, "info")
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
