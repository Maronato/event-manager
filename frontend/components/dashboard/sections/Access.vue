<template>
    <div>
        <v-divider />
        <br />
        <div class="header divided big-title">Acesso</div>
        <div
            class="description"
        >Não corra o risco de perder sua conta. Associe outros serviços e guarde seu token em um local seguro.</div>
        <div class="header my-2">Acesso por Token</div>Seu Token:
        <code>{{ $auth.user.token }}</code>
        <br />
        <v-btn
            size="small"
            class="my-2 white--text"
            tile
            color="red"
            @click="changeToken">Trocar Token</v-btn>
        <div class="header my-2">Acesso pelo Facebook</div>
        <v-btn
            :loading="loadingSocial.facebook"
            :disabled="loadingSocial.facebook"
            class="mb-2 white--text"
            tile
            color="blue"
            @click="fbLogin">
            <v-icon left>fab fa-facebook-f</v-icon>
            {{ fb_text }}
        </v-btn>
        <div class="header my-2">Acesso pelo GitHub</div>
        <v-btn
            :loading="loadingSocial.github"
            :disabled="loadingSocial.github"
            class="mb-2 white--text"
            tile
            color="black"
            @click="ghLogin">
            <v-icon left>fab fa-github</v-icon>
            {{ gh_text }}
        </v-btn>
        <div class="header my-2">Acesso pelo Google</div>
        <v-btn
            :loading="loadingSocial.google"
            :disabled="loadingSocial.google"
            class="mb-2 white--text"
            tile
            color="red"
            @click="goLogin">
            <v-icon left>fab fa-google</v-icon>
            {{ go_text }}
        </v-btn>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                loadingSocial: {
                    facebook: false,
                    github: false,
                    google: false
                }
            }
        },
        computed: {
            fb_text: function() {
                if (this.$auth.user.has_facebook) {
                    return "Desvincular Facebook"
                }
                return "Vincular Facebook"
            },
            gh_text: function() {
                if (this.$auth.user.has_github) {
                    return "Desvincular Github"
                }
                return "Vincular Github"
            },
            go_text: function() {
                if (this.$auth.user.has_google) {
                    return "Desvincular Google"
                }
                return "Vincular Google"
            }
        },
        methods: {
            changeToken() {
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/profiles/change_token/"
                    })
                    .then(data => {
                        this.$toast("Sucesso", "Token alterado :)", "success")
                    })
                    .catch(() => {
                        this.$toast("Opa!", "Algo de errado aconteceu :(", "error")
                    })
            },
            fbLogin() {
                if (this.$auth.user.has_facebook) {
                    this.unlink_social("facebook")
                } else {
                    this.loadingSocial.facebook = true
                    window.location =
                        process.env.API_URL_BROWSER + "/auth/social/login/facebook/"
                }
            },
            ghLogin() {
                if (this.$auth.user.has_github) {
                    this.unlink_social("github")
                } else {
                    this.loadingSocial.github = true
                    window.location =
                        process.env.API_URL_BROWSER + "/auth/social/login/github/"
                }
            },
            goLogin() {
                if (this.$auth.user.has_google) {
                    this.unlink_social("google")
                } else {
                    this.loadingSocial.google = true
                    window.location =
                        process.env.API_URL_BROWSER + "/auth/social/login/google/"
                }
            },
            unlink_social(provider) {
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/social/unlink/",
                        data: {
                            provider: provider
                        }
                    })
                    .then(data => {
                        this.$toast(
                            "Desvinculado",
                            "Seu " + provider + " foi desvinculado",
                            "info"
                        )
                    })
                    .catch(() => {
                        this.$toast("Opa!", "Algo de errado aconteceu :(", "error")
                    })
            }
        }
    }
</script>
