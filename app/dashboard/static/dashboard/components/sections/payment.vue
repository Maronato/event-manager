<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided title">
            Efetuar pagamento
        </div>
        <div class="description">
            <template v-if="user.payment_state == 'Não pago'">
                <b>Atenção!</b> Você ainda precisa efetuar o pagamento até {{ conf_close }}
                <br>
                <b>Não efetuar o pagamento até esse dia significará a perda de seu lugar no evento!</b>
                <br>
                <br>
                <sui-button color="blue" @click="checkout()" content="Efetuar pagamento" />
            </template>
            <template
            v-else-if="user.payment_state == 'Devolvido' ||
            user.payment_state == 'Cancelado'"
            >
                <b>Seu pagamento foi {{ user.payment_state }}</b>. Você pode reefetuar o pagamento até {{ conf_close }} para participar do evento.
                <br>
                <br>
                <sui-button color="blue" @click="checkout()" content="Reefetuar pagamento" />
            </template>
            <template v-else>
                <b>O status do seu pagamento é: {{ user.payment_state }}</b>. Te notificaremos quando ele for alterado.
            </template>
        </div>
        <br>
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf';
    import toast from 'project/js/notifications';
    import * as mome from 'moment';
    import 'moment/locale/pt-br';

    if ("default" in mome) {
        var moment = mome["default"];
    }
    else {
        var moment = mome;
    }

    moment.locale('pt-BR');

    export default {
        props: ['user_context', 'settings_context', 'dashboard_context'],
        data() {
            return {
                user: this.user_context,
                settings: this.settings_context,
                dashboard: this.dashboard_context,
                reg_close_raw: this.settings_context.registration_close_seconds,
                conf_close_raw: this.settings_context.confirmation_seconds
            }
        },
        computed: {
            reg_close() {
                return moment(this.reg_close_raw).calendar();
            },
            conf_close() {
                return moment(this.conf_close_raw).calendar();
            }
        },
        methods: {
            checkout() {
                window.location.href = this.dashboard.urls.checkout
            }
        }
    }
</script>
