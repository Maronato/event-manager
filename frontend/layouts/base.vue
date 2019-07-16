<template>
    <v-app :dark="darkTheme" :light="!darkTheme">
        <slot />
    </v-app>
</template>

<script>
    export default {
        data() {
            return {
                pageTitle: "Login"
            }
        },
        head() {
            return {
                title: this.pageTitle
            }
        },
        computed: {
            darkTheme: {
                get() {
                    return this.$store.state.theme.dark
                },
                set(isDark) {
                    this.$store.commit("theme/setDark", isDark)
                }
            }
        },
        watch: {
            darkTheme() {
                this.$vuetify.theme.dark = this.darkTheme
            }
        }
    }
</script>
