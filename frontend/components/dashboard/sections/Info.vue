<template>
    <div>
        <v-divider />
        <br />
        <div class="header divided big-title">Avisos importantes</div>
        <v-list-item-group color="primary" class="text-xs-left">
            <v-list-item
                v-for="(item, i) in items"
                :key="i"
                :to="item.to"
                :nuxt="item.to"
                :link="item.to || item.href"
                :href="item.href"
                :class="getColor(item)"
                :two-line="Boolean(item.description)">
                <v-list-item-icon v-if="item.icon" :class="getColor(item)">
                    <v-icon v-text="item.icon" />
                </v-list-item-icon>
                <v-list-item-content :class="getColor(item)">
                    <v-list-item-title v-text="item.title" />
                    <v-list-item-subtitle v-if="item.description" v-text="item.description" />
                </v-list-item-content>
            </v-list-item>
        </v-list-item-group>
        <!-- <sui-list-item>O evento começa {{ event_start }} e vai até {{ event_end }}</sui-list-item>
            <sui-list-item><b>O período de check-in é das 9:00 às 19:00, {{ event_start_day }}.</b> Não aceitaremos participantes após esse horário</sui-list-item>
            <sui-list-item><b>Se informe!</b> Leia as <a target="_blank" href="">regras do evento e os critérios de avaliação!</a></sui-list-item>
            <sui-list-item>
                Precisa de mais informações? <a target="_blank" href="https://mte.org.br/contato/">Fale conosco</a>!
            </sui-list-item>
        </sui-list>-->
        <br />
    </div>
</template>
<script>
    export default {
        computed: {
            event_start() {
                return this.$moment(
                    this.$store.state.settings.settings.hackathon_start_seconds
                ).calendar()
            },
            event_start_day() {
                return this.$moment(
                    this.$store.state.settings.settings.hackathon_start_seconds
                ).calendar()
            },
            event_end() {
                return this.$moment(
                    this.$store.state.settings.settings.hackathon_end_seconds
                ).calendar()
            },
            items() {
                return [
                    {
                        title: "O evento começa " + this.event_start,
                        description: "test",
                        icon: "fas fa-clock",
                        color: 'red'
                    },
                    {
                        title: "O evento começa " + this.event_start,
                        description: "",
                        icon: ""
                    }
                ]
            }
        },
        methods: {
            getColor(item) {
                if (item.color) {
                    return item.color + '--text'
                } else {
                    return ''
                }
            }
        },
    }
</script>
