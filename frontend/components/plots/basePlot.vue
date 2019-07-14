<template>
    <v-container>
        <v-card>
            <v-container>
                <h4 class="subheading font-weight-light text-xs-center">{{ title }}</h4>
                <plotly
                    :data="data"
                    :layout="layout"
                    :options="options"
                    :auto-resize="true" />
                <v-layout v-show="loading" text-xs-center>
                    <v-overlay absolute>
                        <v-progress-circular indeterminate size="64"></v-progress-circular>
                        <br />Carregando...
                    </v-overlay>
                </v-layout>
            </v-container>
        </v-card>
    </v-container>
</template>

<script>
    import Plotly from "~/components/vendor/vue-plotly/Plotly"
    import { lightLayout, darkLayout } from "~/components/vendor/vue-plotly/themes"
    export default {
        components: { Plotly },
        props: {
            title: {
                type: String,
                default: ""
            },
            loading: {
                type: Boolean
            }
        },
        computed: {
            data() {
                return this.getData()
            },
            layout() {
                let layout = JSON.parse(JSON.stringify(this.getLayout()))
                if (this.$store.state.theme.appColor === "dark") {
                    layout = darkLayout(layout)
                } else {
                    layout = lightLayout(layout)
                }
                return layout
            },
            options() {
                return this.getOptions()
            }
        },
        methods: {
            getData() {
                return []
            },
            getLayout() {
                return {
                    title: this.title,
                    showlegend: true
                }
            },
            getOptions() {
                return { displaylogo: false, responsive: true }
            }
        }
    }
</script>
