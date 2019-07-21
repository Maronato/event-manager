<template>
    <v-app :dark="darkTheme" :light="!darkTheme">
        <slot />
    </v-app>
</template>

<script>
    export default {
        data() {
            return {
                cookieListener: null
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
            this.sessionLogin()
            this.registerNotifyCookies()
        },
        beforeDestroy() {
            this.unregisterNotifyCookies()
        },
        methods: {
            decode_django_cookie(val) {
                if (val.indexOf("\\") === -1) {
                    return val // not encoded
                }
                val = val.replace(/\\"/g, '"')
                val = val.replace(/\\(\d{3})/g, function(match, octal) {
                    return String.fromCharCode(parseInt(octal, 8))
                })
                return val.replace(/\\\\/g, "\\")
            },
            notifyCookies() {
                let messages = this.$cookies.get("messages")
                if (messages && !Array.isArray(messages)) {
                    messages = JSON.parse(this.decode_django_cookie(messages))
                }
                if (Array.isArray(messages)) {
                    messages.forEach(message => {
                        this.$toast("", message[3], message[2])
                    })
                }
                this.$cookies.remove("messages")
            },
            registerNotifyCookies() {
                this.cookieListener = setInterval(this.notifyCookies, 1000)
            },
            unregisterNotifyCookies() {
                clearInterval(this.cookieListener)
            },
            sessionLogin() {
                if (this.$auth.loggedIn) {
                    this.$auth.request({
                        method: "post",
                        url: "/auth/token/login/",
                        data: {
                            token: this.$auth.user.token
                        }
                    })
                }
            }
        }
    }
</script>
