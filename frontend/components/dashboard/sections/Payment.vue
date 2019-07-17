<template>
    <div>
        <v-divider />
        <br>
        <div class="header divided big-title">
            Efetuar pagamento
        </div>
        <div class="description">
            <template v-if="$auth.user.payment_state == 'Não pago'">
                <b>Atenção!</b> Você ainda precisa efetuar o pagamento até {{ conf_close }}
                <br>
                <b>Não efetuar o pagamento até esse dia significará a perda de seu lugar no evento!</b>
                <br>
                <br>
                <v-btn
                    color="blue"
                    class="white--text"
                    tile
                    :href="apiURL + `/payment/pagseguro/checkout/`">Efetuar pagamento</v-btn>
            </template>
            <template
                v-else-if="$auth.user.payment_state == 'Devolvido' ||
                    $auth.user.payment_state == 'Cancelado'"
            >
                <b>Seu pagamento foi {{ $auth.user.payment_state }}</b>. Você pode reefetuar o pagamento até {{ conf_close }} para participar do evento.
                <br>
                <br>
                <v-btn
                    color="blue"
                    class="white--text"
                    tile
                    :href="apiURL + `/payment/pagseguro/checkout/`">Reefetuar pagamento</v-btn>
            </template>
            <template v-else>
                <b>O status do seu pagamento é: {{ $auth.user.payment_state }}</b>. Te notificaremos quando ele for alterado.
            </template>
        </div>
        <br>
    </div>
</template>

<script>
    export default {
        computed: {
            reg_close() {
                return this.$moment(this.$store.state.settings.settings.registration_close_seconds).calendar();
            },
            conf_close() {
                return this.$moment(this.$store.state.settings.settings.confirmation_seconds).calendar();
            },
            apiURL() {
                return process.env.API_URL_BROWSER
            }
        }
    }
</script>
