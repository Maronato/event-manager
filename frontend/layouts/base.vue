<template>
    <v-app :dark="darkTheme" :light="!darkTheme">
        <slot />
    </v-app>
</template>

<script>
    export default {
        data() {
            return {
                pageTitle: "Login",
                cookieListener: null
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
        },
        mounted() {
            this.registerNotifyCookies()
        },
        beforeDestroy() {
            this.unregisterNotifyCookies()
        },
        methods: {
            notifyCookies() {
                let messages = this.$cookies.get('messages')
                if (messages) {
                    messages = JSON.parse(messages.split('\\054').join(',').split('\\').join(''))
                }
                if (Array.isArray(messages)) {
                    messages.forEach(message => {
                        this.$toast('', message[3], message[2])
                    })
                }
                this.$cookies.remove('messages')
            },
            registerNotifyCookies() {
                this.cookieListener = setInterval(this.notifyCookies, 1000);
            },
            unregisterNotifyCookies() {
                clearInterval(this.cookieListener)
            }
        },
    }
</script>
