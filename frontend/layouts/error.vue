<template>
    <v-container fill-height style="height: calc(100vh - 58px);">
        <v-layout align-center>
            <v-flex text-xs-center>
                <h1 :class="`display-2 ` + color + `--text`">Whoops, {{ error.statusCode }}</h1>
                <p v-if="error.statusCode === 404">{{ pageNotFound }}</p>
                <p v-else>{{ otherError }}</p>
                <v-btn
                    :to="`/`"
                    text
                    outlined
                    :color="color"
                >Voltar à página inical</v-btn>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    export default {
        layout: "empty",
        props: {
            error: {
                type: Object,
                default: null
            }
        },
        head() {
            const title =
                this.error.statusCode === 404 ? this.pageNotFound : this.otherError
            return {
                title
            }
        },
        data() {
            return {
                pageNotFound: "A página que você estava procurando não existe :(",
                otherError: "Algo de errado aconteceu!"
            }
        },
        computed: {
            color() {
                if (this.error.statusCode === 404) {
                    return 'primary'
                } else {
                    return 'red'
                }
            }
        }
    }
</script>

<style scoped>
    h1 {
        font-size: 20px;
    }
</style>
