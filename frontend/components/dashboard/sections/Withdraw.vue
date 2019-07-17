<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided big-title">
            Não poderá participar?
        </div>
        <div class="description">
            <b>Nos avise!</b> Assim poderemos cancelar sua inscrição e liberar a vaga para outra pessoa :)
            <br>
            Você ainda pode mudar de ideia até {{ conf_close }}.
            <template v-if="settings.require_payment">
                <br>
                <b>
                    Nós vamos extornar seu ticket imediatamente caso você desista do evento.
                </b>
            </template>
        </div>
        <br>
        <sui-button
            primary
            :loading="loading"
            :disabled="loading"
            content="Desculpe, não vou conseguir"
            @click="withdraw()" />
        <br>
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf';
    import toast from 'project/js/notifications';
    import * as mome from 'moment';
    import 'moment/locale/pt-br';

    if ("default" in mome) {
        var moment = mome.default;
    }
    else {
        var moment = mome;
    }

    moment.locale('pt-BR');

    export default {
        props: ['userContext', 'settingsContext', 'dashboardContext'],
        data() {
            return {
                user: this.user_context,
                settings: this.settings_context,
                dashboard: this.dashboard_context,
                conf_close_raw: this.settings_context.confirmation_seconds,
                loading: false
            }
        },
        computed: {
            conf_close() {
                return moment(this.conf_close_raw).calendar();
            }
        },
        methods: {
            withdraw() {
                self = this;
                self.loading = true
                axios.post(this.dashboard.api.withdraw)
                    .then(function (data) {
                        toast('Que pena :(', data.data.message, 'info');
                        self.user.state = data.data.state;
                        self.loading = false
                    })
                    .catch(function (error) {
                        console.log(error);
                        toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                        self.loading = false
                    });
            }
        }
    }
</script>
